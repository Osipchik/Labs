using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Lab_1_2
{
    class Program
    {
        private enum Operations
        {
            Sum, Sub, Mul, Div
        }
        
        private static void Main(string[] args)
        {
            if (!ReadArgs(args, out var numbers))
            {
                Console.WriteLine($"Incorrect input: {string.Join(", ", numbers)} it must be 2 integers");   
                return;
            }
            Console.WriteLine($"First binary number: {new Binary(Math.Abs(numbers[0]))}");
            Console.WriteLine($"Second binary number: {new Binary(Math.Abs(numbers[1]))}");
            Console.WriteLine($"Complement code for 1st number: {new Binary(numbers[0])}");
            Console.WriteLine($"Complement code for 2st number: {new Binary(numbers[1])}");
            Console.WriteLine($"Mul of two completion: {Calculate(numbers, Operations.Mul)}");
            Console.WriteLine($"Mul of two decimals: {numbers[0] * numbers[1]}");
        }
        
        
        private static bool ReadArgs(IEnumerable<string> args, out decimal[] numbers)
        {
            var number = new List<decimal>();
            foreach (var s in args)
            {
                if (decimal.TryParse(s, out var num))
                {
                    number.Add(num);
                }
            }
         
            numbers = number.ToArray();
            return numbers.Length == 2;
        }
        
        private static Binary Calculate(IReadOnlyList<decimal> numbers, Operations operation)
        {
            return operation switch
            {
                Operations.Sum => new Binary(numbers[0]) + new Binary(numbers[1]),
                Operations.Sub => new Binary(numbers[0]) + new Binary(numbers[1] * -1),
                Operations.Mul => Mul(numbers[0], numbers[1]),
                _ => throw new ArgumentException($"unknown operation: {operation}")
            };
        }

        private static Binary Mul(decimal num1, decimal num2)
        {
            var res = new Binary(Math.Abs(num1)) * new Binary(Math.Abs(num2));
            return num1 * num2 < 0 ? new Binary(res.ToComplementCode()) : res;
        }
    }
    
    internal class Binary
    {
        private enum NumberSystem
        {
            Base = 2,
            AddedLength = 4,
            MaxSystemLength = 64
        }

        private const int Base = (int) NumberSystem.Base;

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

            return NormalizeNumber(binary, 0);
        }

        private static IEnumerable<int> NormalizeNumber(IList<int> binary, int value)
        {
            if (binary.Count >= (int) NumberSystem.MaxSystemLength) return binary;
            var binaryCount = Math.Abs(binary.Count % (int) NumberSystem.AddedLength - (int) NumberSystem.AddedLength);
            binaryCount += binaryCount == 0 && binary[0] != 0 ? (int) NumberSystem.AddedLength : 0;

            return binary.ExpandFromBegin(binaryCount, value);
        }
        
        private Binary ToInvertCode()
        {
            var binary = new int[Value.Count()];
            var count = 0;
            foreach (var i in Value)
            {
                binary[count++] = i == 1 ? 0 : 1;
            }
            
            return new Binary(NormalizeNumber(binary, 1));
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
            
            return new Binary(CalculateSum(item1, item2));
        }

        private static List<int> CalculateSum(List<int> list1, List<int> list2)
        {
            var addToNext = 0;
            for (var i = list1.Count - 1; i >= 0; i--)
            {
                list1[i] = Add(list1[i] += list2[i] + addToNext, out var add);
                addToNext = add;
            }

            return list1;
        }

        public static Binary operator *(Binary binary1, Binary binary2)
        {
            var (item1, item2) = NormalizeLists(binary1, binary2);
            var res = new List<int>().ExpandFromBegin(item1.Count);
            foreach (var i in item2)
            {
                res = res.ExpandFromEnd(1);
                item1 = item1.ExpandFromBegin(1);
                if (i != 0)
                {
                    res = CalculateSum(res, item1);
                }
            }

            res = NormalizeNumber(res, 0).ToList();
            var range = res.Count - binary1.Value.Count() - binary2.Value.Count();
            res.RemoveRange(0, range > 0 ? range : 0);
            return new Binary(res);
        }

        private static List<int> NormalizeBinary(Binary binary, int lenSub)
        {
            var bin = binary.Value.ToList();
            
            return bin.ExpandFromBegin(lenSub, bin[0] == 1 && bin[1] == 1 ? 1 : 0);
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