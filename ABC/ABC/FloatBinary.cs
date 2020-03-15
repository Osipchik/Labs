using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace ABC
{
    public class FloatBinary
    {
        private enum BinaryConstants
        {
            Base = 2,
            Exponent = 11,
            Mantissa = 52,
            Exp = 1023
        }
        
        private static readonly int[] ZeroExp = new int[(int) BinaryConstants.Exponent];
        private static readonly int[] ZeroMantissa = new int[(int) BinaryConstants.Mantissa];

        private bool _isNegative;
        private IEnumerable<int> _exponent;
        private IEnumerable<int> _mantissa;

        public FloatBinary(double number)
        {
            _isNegative = number < 0;
            if (Math.Abs(number) > 0)
            {
                var num = Math.Truncate(number);
                var wholeNum = new Binary(Math.Abs(num)).Value;
                var fraction = GetFraction(number - num);
                CreateNum(wholeNum, fraction);
            }
            else
            {
                _exponent = ZeroExp;
                _mantissa = ZeroMantissa;
            }
        }

        private FloatBinary(bool isNegative, IEnumerable<int> exponent, IEnumerable<int> mantissa)
        {
            _isNegative = isNegative;
            _exponent = exponent;
            _mantissa = mantissa;
        }

        private static IEnumerable<int> GetFraction(double number)
        {
            var num = Math.Abs(number);
            var mantissa = new List<int>();
            while (mantissa.Count != (int) BinaryConstants.Exp)
            {
                num *= (int) BinaryConstants.Base;
                mantissa.Add(num >= 1 ? 1 : 0);
                num -= Math.Truncate(num);
            }
            
            return mantissa;
        }

        private void CreateNum(IEnumerable<int> wholeNum, IEnumerable<int> fraction)
        {
            var num = wholeNum.ToArray();
            var bin = new List<int>(num);
            bin.AddRange(fraction);
            var spaces = bin.IndexOf(1) + 1;
            _exponent = (new Binary(num.Length - spaces) + new Binary((int) BinaryConstants.Exp)).Value;
            _mantissa = ExpandMantissa(bin.ToList().GetRange(spaces, bin.Count - spaces));
        }

        private static IEnumerable<int> ExpandMantissa(IEnumerable<int> mantissa)
        {
            var m = mantissa.ToList();
            var count = m.Count;
            if (count < (int) BinaryConstants.Mantissa) m.AddRange(new int[(int) BinaryConstants.Mantissa - m.Count]); 

            return m.GetRange(0, (int) BinaryConstants.Mantissa).ToArray();
        }

        public static FloatBinary operator +(FloatBinary fb1, FloatBinary fb2)
        {
            if (fb1.CheckZero()) return fb2;
            if (fb2.CheckZero()) return fb1;
            NormalizeNums(ref fb1, ref fb2, out var expDif);

            return AddSignificands(fb1, fb2, expDif);
        }

        private static (List<int> m1, List<int> m2) Prepare(FloatBinary fb1, FloatBinary fb2, double expDif) =>
            expDif.CompareTo(0) switch
            {
                1 => ExpandMantissas(fb1, fb2, new[] {1, 0}),
                -1 => ExpandMantissas(fb1, fb2, new[] {0, 1}),
                _ => ExpandMantissas(fb1, fb2, new[] {1, 1})
            };

        private static (List<int> m1, List<int> m2) ExpandMantissas(FloatBinary fb1, FloatBinary fb2, int[] insert)
        {
            var m1 = fb1._mantissa.ToList();
            var m2 = fb2._mantissa.ToList();
            m1.InsertRange(0, new []{0, insert[0]});
            m2.InsertRange(0, new []{0, insert[1]});

            return (m1, m2);
        }

        private static FloatBinary AddSignificands(FloatBinary fb1, FloatBinary fb2, double expDif)
        {
            var exp = fb1._exponent;
            var (m1, m2) = Prepare(fb1, fb2, expDif);

            var firstBigger = Math.Abs(fb1.ToDouble) > Math.Abs(fb2.ToDouble);
            if (!fb1._isNegative && fb2._isNegative || fb1._isNegative && !fb2._isNegative)
                GetComplementCode(ref firstBigger ? ref m1 : ref m2);
            
            var res = (new Binary(m1) + new Binary(m2)).Value.ToList();

            if(!fb1._isNegative && !fb2._isNegative || fb1._isNegative && fb2._isNegative) NormalizePositive(ref exp, ref res);
            else NormalizeNegative(ref exp, ref res);
            fb1._isNegative = firstBigger ? fb1._isNegative : fb2._isNegative;
            
            return new FloatBinary(fb1._isNegative, exp, res);
        }

        private static void GetComplementCode(ref List<int> m)
        {
            m = new Binary(m).ToComplementCode().ToList();
            m.Insert(0, 0);
        }

        private static void NormalizePositive(ref IEnumerable<int> exp, ref List<int> res)
        {
            if (res[0] == 1)
            {
                exp = IncrementExponent(exp, 1);
                res.RemoveAt(0);
                res.RemoveAt(res.Count - 1);
            }
            else if (res[1] == 1) res.RemoveRange(0, 2);
        }

        private static void NormalizeNegative(ref IEnumerable<int> exp, ref List<int> sub)
        {
            Console.WriteLine($"sub: {new Binary(sub)}");
            if (sub[0] == 0 && sub[1] == 1)
            {
                sub.RemoveAt(0);
                sub = new Binary(sub).ComplementToDirect.Value.ToList();
            }
            sub.RemoveAt(0);
            exp = IncrementExponent(exp, 1);
            var index = sub.IndexOf(1);
            if (index >= (int) BinaryConstants.Mantissa || index < 0)
            {
                exp = ZeroExp;
                sub = ZeroMantissa.ToList();
            }
            else
            {
                exp = DecrementExponent(exp, index+1);
                sub.RemoveRange(0, index + 1);
                sub.AddRange(new int[(int) BinaryConstants.Mantissa - sub.Count]);
            }
            
            //0100 0001 1100  1001 1100 0001 0100 1101 1100 1101 1001 0001 0110 0001 1111 1010

        }
        
        private static void NormalizeNums(ref FloatBinary fb1, ref FloatBinary fb2, out double expDiff)
        {
            expDiff = fb1.GetExponent - fb2.GetExponent;
            if (expDiff > 0) fb2 = MakeExponentsEqual(fb2, (int) expDiff);
            else if (expDiff < 0) fb1 = MakeExponentsEqual(fb1, (int) expDiff);
        }

        private static FloatBinary MakeExponentsEqual(FloatBinary floatBinary, int difference)
        {
            difference = Math.Abs(difference);
            var exponent = floatBinary._exponent;
            var mantissa = floatBinary._mantissa.ToList();
            if (difference >= 0)
            {
                exponent = IncrementExponent(exponent, difference);
                mantissa = ShiftMantissa(mantissa, difference);
                mantissa.RemoveAt(0);
            }
            
            return new FloatBinary(floatBinary._isNegative, exponent, mantissa);
        }

        private static List<int> ShiftMantissa(List<int> mantissa, int count, bool addOne = true)
        {
            if (count < (int) BinaryConstants.Mantissa)
            {
                if (addOne) mantissa.Insert(0, 1);
                mantissa.RemoveRange(mantissa.Count - 1 - count, count);
                mantissa.InsertRange(0, new int[count]);
            }
            else mantissa = new List<int>(new int[(int) BinaryConstants.Mantissa + 1]);

            return mantissa;
        }

        private static IEnumerable<int> IncrementExponent(IEnumerable<int> exponent, int count)
        {
            var exp = exponent.ToList();
            exp = (new Binary(exp) + new Binary(count)).Value.ToList();
            if (exp[0] != 0) throw new OverflowException("exponent overflow");
            
            return exp;
        }

        private static IEnumerable<int> DecrementExponent(IEnumerable<int> exponent, int count)
        {
            var exp = exponent.ToList();
            exp = (new Binary(exp) + new Binary(-count)).Value.ToList();
            if (exp.TakeWhile(i => i == 0).Count() == exp.Count) throw new OverflowException("exponent underflow");
            
            return (new Binary(exp) + new Binary(-count)).Value.ToList();;
        }
        

        public override string ToString()
        {
            var exp = Regex.Replace(string.Join("", _exponent), ".{4}", "$0 ");
            var mantissa = Regex.Replace(string.Join("", _mantissa), ".{4}", "$0 ");

            return $"{Convert.ToInt16(_isNegative)}  {exp} {mantissa}";
        }

        private double GetExponent => (new Binary(_exponent) + new Binary(-(int) BinaryConstants.Exp)).ToDouble();
        
        private bool CheckZero() => _exponent.Compare(ZeroExp) && _mantissa.Compare(ZeroMantissa);
        
        public double ToDouble => CheckZero() ? 0 : ConvertToDouble();

        private double ConvertToDouble()
        {
            var exponent = GetExponent;
            var res = 1.0;
            var pow = -1;
            foreach (var i in _mantissa)
            {
                if (i == 1) res += Math.Pow((int) BinaryConstants.Base, pow);
                pow--;
            }
            res *= Math.Pow((int) BinaryConstants.Base, exponent);

            return _isNegative ? -res : res;
        }

        public static explicit operator Binary(FloatBinary b)
        {
            var bin = new List<int> {Convert.ToInt16(b._isNegative)};
            bin.AddRange(b._exponent);
            bin.AddRange(b._mantissa);
            
            return new Binary(bin);
        }
    }
}