﻿using System;
using System.Collections.Generic;

namespace ABC
{
    public class ConsoleMain
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
}