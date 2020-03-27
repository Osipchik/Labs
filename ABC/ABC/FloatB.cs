using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using Microsoft.CSharp.RuntimeBinder;

namespace ABC
{
    public class FloatB
    {
        private enum BinaryConstants
        {
            Base = 2,
            Exponent = 11,
            Mantissa = 52,
            Exp = 1023
        }
        
        // private enum BinaryConstants
        // {
        //     Base = 2,
        //     Exponent = 8,
        //     Mantissa = 23,
        //     Exp = 127
        // }

        private readonly bool _isNegative;
        private IEnumerable<int> _exponent;
        private IEnumerable<int> _mantissa;
        private static IEnumerable<int> zeroExp = new int[(int) BinaryConstants.Exponent];
        private static IEnumerable<int> zeroMan = new int[(int) BinaryConstants.Mantissa];
        
        
        public FloatB(double num)
        {
            _isNegative = num < 0;
            if (num != 0)
            {
                var (exp, mantissa) = CreateNum(new Bin(Math.Truncate(Math.Abs(num))).ValueBin, GetFraction(num));
                _exponent = exp;
                _mantissa = mantissa;
            }
            else
            {
                _exponent = zeroExp;
                _mantissa = zeroMan;
            }
        }

        private FloatB(bool isNegative, IEnumerable<int> exponent, IEnumerable<int> mantissa)
        {
            _isNegative = isNegative;
            _exponent = exponent;
            _mantissa = mantissa;
        }

        private static IEnumerable<int> GetFraction(double number)
        {
            number = Math.Abs(number);
            number -= Math.Truncate(number);
            var mantissa = new List<int>();
            while (mantissa.Count != (int) BinaryConstants.Exp)
            {
                number *= (int) BinaryConstants.Base;
                mantissa.Add(number >= 1 ? 1 : 0);
                number -= Math.Truncate(number);
            }

            return mantissa;
        }
        
        private static (IEnumerable<int> exp, IEnumerable<int> mantissa) CreateNum(IEnumerable<int> wholeNum, IEnumerable<int> fraction)
        {
            var num = wholeNum.ToArray();
            var bin = new List<int>(num);
            bin.AddRange(fraction);
            var spaces = bin.IndexOf(1) + 1;
            var exponent = num.Length - spaces + (int) BinaryConstants.Exp;
            var exp = NormalizeBin(new Bin(exponent).ValueBin, (int) BinaryConstants.Exponent, false);
            var mantissa = NormalizeBin(bin.ToList().GetRange(spaces, bin.Count - spaces), (int) BinaryConstants.Mantissa);

            return (exp, mantissa);
        }

        private static IEnumerable<int> NormalizeBin(IEnumerable<int> mantissa, int size, bool fromEnd = true)
        {
            var m = mantissa.ToList();
            if (m.Count < size)
            {
                var add = new int[size - m.Count];
                if (fromEnd) m.AddRange(add); 
                else m.InsertRange(0, add);
            }

            return m.GetRange(0, size);
        }

        public static FloatB operator /(FloatB fb1, FloatB fb2)
        {
            if (IsZero(fb2))
            {
                throw new DivideByZeroException("Attempted to divide by zero.");
            }
            if (IsZero(fb1))
            {
                return new FloatB(fb1._isNegative != fb2._isNegative, zeroExp, zeroMan);
            }
            
            var exp = CalculateExponent(fb1, fb2).ToList();
            var mantissa = CalculateMantissa(fb1, fb2).ToList();
            var (e, m) = NormalizeDiv(exp, mantissa);
            
            return new FloatB(fb1._isNegative != fb2._isNegative, e, m);
        }

        private static IEnumerable<int> CalculateMantissa(FloatB fb1, FloatB fb2)
        {
            var m1 = fb1._mantissa.ToList();
            var m2 = fb2._mantissa.ToList();
            m1.InsertRange(0, new [] {0, 1});
            m2.InsertRange(0, new [] {0, 1});
            var mantissa = (new Binary(m1) / new Binary(m2)).Value.ToList();

            if (mantissa[0] == 1 && mantissa[1] == 0)
            {
                mantissa.RemoveRange(0, 1);
                mantissa.RemoveAt(mantissa.Count - 1);
            }
            else if (mantissa[0] == 0 && mantissa[1] == 1)
            {
                mantissa.RemoveRange(0, 2);
            }
            
            if (mantissa.Count < (int) BinaryConstants.Mantissa)
            {
                mantissa.AddRange(new int[(int) BinaryConstants.Mantissa - mantissa.Count]);
            }

            return mantissa;
        }

        private static IEnumerable<int> CalculateExponent(FloatB fb1, FloatB fb2)
        {
            var exp = fb1.GetExponent - fb2.GetExponent + (int) BinaryConstants.Exp;
            var exponent = new Bin(exp).ValueBin.ToList();
            
            if (exponent.Count > (int) BinaryConstants.Exponent)
            {
                throw new OverflowException("Overflow");
            }

            return exponent;
        }

        private static (IEnumerable<int> e, IEnumerable<int> m) NormalizeDiv(List<int> exp, List<int> mantissa)
        {
            if (exp.Count < (int) BinaryConstants.Exponent)
            {
                exp.InsertRange(0, new int[(int) BinaryConstants.Exponent - exp.Count]);
            }

            CheckUnderflow(exp);

            var dif = (int) BinaryConstants.Mantissa - mantissa.Count;
            if (dif < 0)
            {
                exp.Insert(0, 0);
                exp = (new Binary(exp) + new Binary(dif)).Value.ToList();
                exp.RemoveAt(0);
                CheckUnderflow(exp);
            }
            
            
            return (exp, mantissa);
        }

        private static void CheckUnderflow(IEnumerable<int> exp)
        {
            var asd = exp.ToList();
            if (asd.TakeWhile(i => i == 0).Count() == (int) BinaryConstants.Exponent)
            {
                throw new OverflowException("Underflow");
            }
        }
        
        private double GetExponent => new Bin(_exponent).ToDouble() - (int) BinaryConstants.Exp;

        private static bool IsZero(FloatB fb)
        {
            var e = fb._exponent.TakeWhile(i => i == 0).Count();

            return e == (int) BinaryConstants.Exponent;
        }
        
        public double ToDouble()
        {
            if (IsZero(this))
            {
                return 0;
            }
            
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
        
        public override string ToString()
        {
            var exp = Regex.Replace(string.Join("", _exponent), ".{4}", "$0 ");
            var mantissa = Regex.Replace(string.Join("", _mantissa), ".{4}", "$0 ");
            return $"{Convert.ToInt16(_isNegative)}  {exp}  {mantissa}";
        }
    }
}