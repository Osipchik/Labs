using System;
using System.Collections.Generic;

namespace ABC
{
    public static class ConsoleMain
    {
        private enum Operations
        {
            Sum, Sub, Mul, Div
        }

        private static void Main(string[] args)
        {
            if (!ReadArgs(args, out var numbers))
            {
                Console.WriteLine($"Incorrect input: {string.Join(", ", numbers)} it must be 2 floats");   
                return;
            }
                
            Console.WriteLine($"1st binary number: {new FloatBinary(numbers[0])}");
            Console.WriteLine($"2nd binary number: {new FloatBinary(numbers[1])}");
            try
            {
                var asd = Calculate(numbers, Operations.Sum);
                Console.WriteLine($"Sum of two floats: {asd}");
                Console.WriteLine($"Sum of two float converted to dec: {asd.ToDouble}");
                Console.WriteLine($"Sum of two dec (using c#): {numbers[0] + numbers[1]}");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
            
        private static bool ReadArgs(IEnumerable<string> args, out double[] numbers)
        {
            var number = new List<double>();
            foreach (var s in args) if (double.TryParse(s, out var num)) number.Add(num);
            numbers = number.ToArray();
                
            return numbers.Length == 2;
        }
            
        private static FloatBinary Calculate(IReadOnlyList<double> numbers, Operations operation)
        {
            return operation switch
            {
                Operations.Sum => new FloatBinary(numbers[0]) + new FloatBinary(numbers[1]),
                // Operations.Sub => new Binary(numbers[0]) + new Binary(-numbers[1]),
                // Operations.Mul => new Binary(numbers[0]) * new Binary(numbers[1]),
                // Operations.Div => new Binary(numbers[0]) / new Binary(numbers[1]),
                _ => throw new ArgumentException($"unknown operation: {operation}")
            };
        }
    }
}