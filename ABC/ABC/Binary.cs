using System;
using System.Collections.Generic;
using System.Linq;
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
        
        private IEnumerable<int> Value { get; }

        public Binary(decimal num) 
        {
            Value = num < 0 ? ToDirectCode(-num) : ToDirectCode(num);
            if (num < 0)
            {
                Value = ToComplementCode();
            }
        }

        private Binary(IEnumerable<int> binary)
        {
            Value = binary;
        }
        
        private static IEnumerable<int> ToDirectCode(decimal num)
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
        
        private Binary ToInvertCode()
        {
            var binary = new int[Value.Count()];
            var count = 0;
            foreach (var i in Value)
            {
                binary[count++] = i == 1 ? 0 : 1;
            }
            
            return new Binary(binary);
        }

        private IEnumerable<int> ToComplementCode()
        {
            var code = this;
            if (Value.First() != 1)
            {
                code = ToInvertCode() + new Binary(1);
                code.Value.ToArray()[0] = 1;
            }
            
            return code.Value;
        }

        public Binary ComplementToDirect => Value.First() != 1 ? this : (this + new Binary(-1)).ToInvertCode();
        
        public static Binary operator +(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1, binary2);
            var res = CalculateSum(item1, item2);

            return new Binary(res);
        }
        
        public static Binary operator *(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1, binary2);
            var res = new List<int>().ExpandBegin(item1.Count);
            var shift = 0;
            item2.Reverse();
            foreach (var i in item2)
            {
                if (i != 0)
                {
                    var shifted = item1.GetRange(shift, item1.Count - shift).ExpandEnd(shift);
                    res = CalculateSum(res, shifted);
                }
                shift++;
            }

            var range = res.IndexOf(1);
            return new Binary(NormalizeNumber(res.GetRange(range, res.Count - range)).ToList());
        }

        public static Binary operator /(Binary binary1, Binary binary2)
        {
            if (!SqueezeBin(binary2.Value).Any())
            {
                throw new DivideByZeroException("Attempted to divide by zero.");
            }
            
            var sign = binary1.Value.First() == binary2.Value.First();
            var binNum = binary1.ComplementToDirect.Value.ToArray();

            var divider = binary2.Value.First() != 1 ? new Binary(binary2.ToComplementCode()) : binary2;

            var res = GetIntPath(binNum, divider, out _);

            var asd = sign ? NormalizeNumber(SqueezeBin(res)) : new Binary(res).ToComplementCode();
            return new Binary(asd);
        }

        private static IEnumerable<int> GetIntPath(IEnumerable<int> dividendNum, Binary divider, out List<int> dividend)
        {
            var res = new List<int>();
            dividend = new List<int>();
            foreach (var i in dividendNum)
            {
                dividend.Add(i);
                var remains = new Binary(NormalizeNumber(dividend)) + divider;
                if (remains.Value.First() != 1)
                {
                    dividend = remains.Value.ToList();
                    res.Add(1);
                }
                else
                {
                    res.Add(0);
                }
            }

            return res;
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

        private static List<int> CalculateSum(List<int> list1, List<int> list2)
        {
            var addToNext = 0;
            for (var i = list1.Count - 1; i >= 0; i--)
            {
                list1[i] = Add(list1[i] += list2[i] + addToNext, out var add);
                addToNext = add;
            }

            if (list1.Count >= (int) BinarySystem.MaxLength && addToNext != 0)
            {
                throw new OverflowException("Overflow");
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
    
    public static class Extensions
    {
        public static List<int> ExpandBegin(this IEnumerable<int> list, int discharge, int value = 0)
        {
            var expandedList = GenerateList(discharge, value).ToList();
            expandedList.AddRange(list);
            return expandedList;
        }
        
        public static List<int> ExpandEnd(this IEnumerable<int> list, int discharge, int value = 0)
        {
            var expandedList = new List<int>(list);
            expandedList.AddRange(GenerateList(discharge, value));
            return expandedList;
        }

        private static IEnumerable<int> GenerateList(int size, int value)
        {
            var arr = new int[size];
            for (var i = 0; i < arr.Length; i++)
            {
                arr[i] = value;
            }

            return arr;
        }
    }
}