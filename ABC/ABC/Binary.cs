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
            ByteLen = 8,
            MaxSystemLength = 64
        }

        private const int Base = (int) BinarySystem.Base;

        private IEnumerable<int> Value { get; }

        public Binary(decimal num) 
        {
            Value = num < 0 ? ToDirectCode(-num) : ToDirectCode(num);
            if (num < 0)
            {
                Value = ToComplementCode();
            }
        }

        public Binary(IEnumerable<int> binary)
        {
            Value = binary;
        }
        
        private static IEnumerable<int> ToDirectCode(decimal num)
        {
            var binary = new List<int>();
            while (num > 0)
            {
                num /= Base;
                binary.Insert(0, Convert.ToInt32(num > Math.Truncate(num)));
                num = Math.Truncate(num);
            }

            return NormalizeNumber(binary);
        }

        private static IEnumerable<int> NormalizeNumber(IList<int> binary)
        {
            return binary.Count >= (int) BinarySystem.MaxSystemLength 
                ? binary 
                : binary.ExpandFromBegin(Math.Abs(binary.Count % (int) BinarySystem.ByteLen - (int) BinarySystem.ByteLen));
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

        public IEnumerable<int> ToComplementCode()
        {
            var code = ToInvertCode();
            code += new Binary(1);
            code.Value.ToArray()[0] = 1;
            
            return code.Value;
        }

        public static Binary operator +(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1, binary2);
            var res = CalculateSum(item1, item2);

            return new Binary(res);
        }

        private static List<int> CalculateSum(List<int> list1, List<int> list2)
        {
            var addToNext = 0;
            for (var i = list1.Count - 1; i >= 0; i--)
            {
                list1[i] = Add(list1[i] += list2[i] + addToNext, out var add);
                addToNext = add;
            }

            if (list1.Count >= (int) BinarySystem.MaxSystemLength && addToNext != 0)
            {
                throw new OverflowException("Overflow");
            }
            return list1;
        }

        public static Binary operator *(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1, binary2);
            var res = new List<int>().ExpandFromBegin(item1.Count);
            var shift = 0;
            item2.Reverse();
            foreach (var i in item2)
            {
                if (i != 0)
                {
                    var shifted = item1.GetRange(shift, item1.Count - shift).ExpandFromEnd(shift);
                    res = CalculateSum(res, shifted);
                }
                shift++;
            }

            var range = res.IndexOf(1);
            return new Binary(NormalizeNumber(res.GetRange(range, res.Count - range)).ToList());
        }

        private static List<int> NormalizeBinary(Binary binary, int lenSub)
        {
            var bin = binary.Value.ToList();
            
            return bin.ExpandFromBegin(lenSub, bin[0] == 1 ? 1 : 0);
        }

        private static (List<int>, List<int>) NormalizeLists(Binary binary1, Binary binary2)
        {
            var bin1 = binary1.Value.ToList();
            var bin2 = binary2.Value.ToList();
            bin1 = bin1.Count < bin2.Count ? NormalizeBinary(binary1, bin2.Count - bin1.Count) : bin1;
            bin2 = bin2.Count < bin1.Count ? NormalizeBinary(binary2, bin1.Count - bin2.Count) : bin2;

            return (bin1, bin2);
        }

        private static int Add(int binItem, out int add)
        {
            add = 0;
            if (binItem >= Base)
            {
                binItem -= Base;
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
        public static List<int> ExpandFromBegin(this IEnumerable<int> list, int discharge, int value = 0)
        {
            var expandedList = GenerateList(discharge, value).ToList();
            expandedList.AddRange(list);
            return expandedList;
        }
        
        public static List<int> ExpandFromEnd(this IEnumerable<int> list, int discharge, int value = 0)
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