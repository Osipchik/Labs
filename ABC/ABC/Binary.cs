using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text.RegularExpressions;

namespace ABC
{
    public class Binary
    {
        private enum BinarySystem
        {
            Base = 2,
            MinLen = 4,
            MaxLength = 64
        }
        
        public IEnumerable<int> Value { get; }

        public Binary(double num) 
        {
            Value = num < 0 ? ToDirectCode(-num) : ToDirectCode(num);
            if (num < 0) Value = ToComplementCode();
        }

        public Binary(IEnumerable<int> binary)
        {
            Value = binary;
        }
        
        private static IEnumerable<int> ToDirectCode(double num)
        {
            var binary = new List<int>();
            while (num > 0)
            {
                num /= (int) BinarySystem.Base;
                binary.Insert(0, Convert.ToInt32(num > Math.Truncate(num)));
                num = Math.Truncate(num);
            }

            return NormalizeNumber(binary);
        }

        private static IEnumerable<int> NormalizeNumber(IEnumerable<int> binary)
        {
            var number = binary.ToList();

            return number.Count >= (int) BinarySystem.MaxLength 
                ? number 
                : number.ExpandBegin(Math.Abs(number.Count % (int) BinarySystem.MinLen - (int) BinarySystem.MinLen));
        }
        
        public Binary ToInvertCode()
        {
            var binary = new int[Value.Count()];
            var count = 0;
            foreach (var i in Value) binary[count++] = i == 1 ? 0 : 1;
            
            return new Binary(binary);
        }

        public IEnumerable<int> ToComplementCode()
        {
            var code = this;
            if (Value.First() != 1)
            {
                code = ToInvertCode() + new Binary(1);
                code.Value.ToList()[0] = 1;
            }
        
            return code.Value;
        }

        public Binary ComplementToDirect => Value.First() != 1 ? this : (this + new Binary(-1)).ToInvertCode();
        
        public static Binary operator +(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1, binary2);
            var res = CalculateSum(item1, item2, out _).ToList();

            return new Binary(res);
        }

        public static Binary operator *(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1.ComplementToDirect, binary2.ComplementToDirect);
            var res = new Binary(new List<int>().ExpandBegin(item1.Count));
            var shift = 0;
            item2.Reverse();
            
            foreach (var i in item2)
            {
                if (i != 0)
                {
                    var shifted = item1.ExpandEnd(shift);
                    res += new Binary(shifted);
                }
                shift++;
            }

            return NormalizeMul(binary1, binary2, new Binary(NormalizeNumber(res.Value)));
        }

        private static Binary NormalizeMul(Binary binary1, Binary binary2, Binary result)
        {
            if (binary1.Value.First() == binary2.Value.First()) result = result.ComplementToDirect;
            else if (binary1.Value.First() != binary2.Value.First() && result.Value.First() != 1)
                result = new Binary(result.ToComplementCode());

            return result;
        }

        public static Binary operator /(Binary binary1, Binary binary2)
        {
            if (!SqueezeBin(binary2.Value).Any()) throw new DivideByZeroException("Attempted to divide by zero.");
            
            var divider = binary2.Value.First() != 1 ? new Binary(binary2.ToComplementCode()) : binary2;
            var res = GetIntPath(binary1.ComplementToDirect.Value, divider, out _);

            return new Binary(res);
        }

        private static IEnumerable<int> GetIntPath(IEnumerable<int> dividendNum, Binary divider, out List<int> dividend)
        {
            var res = new List<int>();
            var num = dividendNum.ToList();
            dividend = new List<int>(num.GetRange(0, divider.Value.Count() - 1));
            
            var count = dividend.Count;
            while (CompareExp(res, 54))
            {
                dividend.Add(count < num.Count ? num[count] : 0);
                var remains = (new Binary(NormalizeNumber(dividend)) + divider).Value.ToList();
                if (remains.First() != 1)
                {
                    dividend = remains;
                    res.Add(1);
                }
                else res.Add(0);
                count++;
            }

            return res;
        }

        private static bool CompareExp(List<int> bin, int exp)
        {
            var index = bin.IndexOf(1);
            
            if (index >= 0)
            {
                var len = bin.GetRange(index, bin.Count - index).Count();
                return len < exp;
            }
            
            return true;
        }

        private static IEnumerable<int> SqueezeBin(IEnumerable<int> bin)
        {
            var list = bin.ToList();
            var index = list.IndexOf(1);
            list.RemoveRange(0, index > 0 ? index : list.Count);
        
            return list;
        }
        
        private static List<int> NormalizeBinary(Binary binary, int lenSub)
        {
            var bin = binary.Value.ToList();
            
            return bin.ExpandBegin(lenSub, bin[0] == 1 ? 1 : 0);
        }

        private static (List<int>, List<int>) NormalizeLists(Binary binary1, Binary binary2)
        {
            var bin1 = binary1.Value.ToList();
            var bin2 = binary2.Value.ToList();
            bin1 = bin1.Count < bin2.Count ? NormalizeBinary(binary1, bin2.Count - bin1.Count) : bin1;
            bin2 = bin2.Count < bin1.Count ? NormalizeBinary(binary2, bin1.Count - bin2.Count) : bin2;

            return (bin1, bin2);
        }

        private static IEnumerable<int> CalculateSum(IList<int> list1, IList<int> list2, out int addToNext)
        {
            addToNext = 0;
            for (var i = list1.Count - 1; i >= 0; i--)
            {
                list1[i] = Add(list1[i] += list2[i] + addToNext, out var add);
                addToNext = add;
            }
            
            return list1;
        }
        
        private static int Add(int binItem, out int add)
        {
            add = 0;
            if (binItem >= (int) BinarySystem.Base)
            {
                binItem -= (int) BinarySystem.Base;
                add = 1;
            }

            return binItem;
        }

        public override string ToString()
        {
            return Regex.Replace(string.Join("", Value), ".{4}", "$0 ");
        }
    }
}