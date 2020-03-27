using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

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
            // var n1 = 2.555d;
            // var n2 = 0.00500d;
            // var asd = new FloatB(n1) / new FloatB(n2);
            // Console.WriteLine(asd);
            // Console.WriteLine(asd.ToDouble());
            // Console.WriteLine("0  1000 0000   0100 0000 0000 0000 0000 000");
            // Console.WriteLine(n1 / n2);
            //
            
            // var asd = new Binary(new []{0,  1,0,0,0, 1,0,0,0}) + new Binary(-1);
            // Console.WriteLine(asd);
            // Console.WriteLine(asd.ToDouble());
            



            if (!ReadArgs(args, out var numbers))
            {
                Console.WriteLine($"Incorrect input: {string.Join(", ", numbers)} it must be 2 floats");   
                return;
            }
                
            Console.WriteLine($"1st binary number: {new FloatB(numbers[0])}");
            Console.WriteLine($"2nd binary number: {new FloatB(numbers[1])}");
            try
            {
                var asd = Calculate(numbers, Operations.Sum);
                Console.WriteLine($"Div of two floats: {asd}");
                Console.WriteLine($"Div of two float converted to dec: {asd.ToDouble()}");
                Console.WriteLine($"Div of two dec (using c#): {numbers[0] / numbers[1]}");
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
            
        private static FloatB Calculate(IReadOnlyList<double> numbers, Operations operation)
        {
            return operation switch
            {
                Operations.Sum => new FloatB(numbers[0]) / new FloatB(numbers[1]),
                _ => throw new ArgumentException($"unknown operation: {operation}")
            };
        }
    }
}