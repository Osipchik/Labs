
using System;
using System.Collections.Generic;

namespace Lab1
{
    class Nums
    {
        public static List<int> Summ(List<int> num1, List<int> num2)
        {
            var result = new List<int>();
            var ONE = false;//Для сохранения 1 при сумме
            if (num1.Count != num2.Count)//Приводим к одинаковой размерности
            {
                var num1_sign = Convert.ToBoolean(num1[0]);
                var num2_sign = Convert.ToBoolean(num2[0]);
                num1.Reverse();
                num2.Reverse();
                while (num2.Count > num1.Count)
                {
                    if (num1_sign)
                        num1.Add(1);
                    else num1.Add(0);
                }
                while (num1.Count > num2.Count)
                {
                    if (num2_sign)
                        num2.Add(1);
                    else num2.Add(0);
                }
                num1.Reverse();
                num2.Reverse();
            }
            for (int i = num1.Count - 1; i >= 0; i--)
            {
                result.Add(num1[i] + num2[i]);
                if (ONE)
                {
                    result[result.Count - 1] += 1;
                    ONE = false;
                }
                if (result[result.Count - 1] == 2)
                {
                    result[result.Count - 1] = 0;
                    ONE = true;
                }
                if (result[result.Count - 1] == 3)
                {
                    result[result.Count - 1] = 1;
                    ONE = true;
                }
            }
            if (result[result.Count - 1] >= 2)
            {
                result[result.Count - 1] = 0;
                result.Add(1);
            }
            result.Reverse();
            return result;
        }

        public static string Multiplication(List<int> num1, List<int> num2)
        {
            List<int> result = new List<int>();
            List<List<int>> multipled_nums = new List<List<int>>();
            List<int> multipled_res = new List<int>();
            int shift = 0;//Сдвиг
            for (int i = num2.Count - 1; i >= 0; i--)
            {
                if (num2[i] == 1)
                {
                    for (int k = shift; k < num1.Count; k++)
                    {
                        multipled_res.Add(num1[k]);
                    }
                    for (int k = 0; k < shift; k++)
                    {
                        multipled_res.Add(0);
                    }

                    Console.WriteLine(shift);
                    Console.WriteLine(string.Join("", multipled_res));
                    multipled_nums.Add(multipled_res);
                    multipled_res = new List<int>();
                }
                shift++;
            }
            // 2
            // 11110100
            // 3
            // 11101000
            // 5
            // 10100000
            // 6
            // 01000000
            // 7
            // 10000000


            Console.WriteLine();
            result.AddRange(multipled_nums[0]);
            for (int i = 1; i < multipled_nums.Count; i++)
            {
                result = Summ(multipled_nums[i], result);
            }
            return string.Join("", result);
        }

        static void Main(string[] args)
        {
            int num1_in_decimal = -3, num2_in_decimal = -20;
            
            var num1InAdcode = new List<int>
            {
                0,0,0,0, 
                0,1,1,1,
                1,1,1,0, 
                0,1,0,1, 
                0,0,0,1, 
                1,0,0,1,
                0,1,1,0, 
                1,1,1,0, 
                0,0,1,0,
                1,0,1,0,
                1,1,1,0,
                0,0,1,1,
                1,0,0,0,
                1,1,1,0
            };
            Console.WriteLine(string.Join("", num1InAdcode));
            var num2InAdcode = new List<int>
            {
                0,0,0,0,
                1,0,1,1,
                1,1,0,1,
                0,1,1,1,
                1,0,1,0,
                0,1,1,0,
                0,0,1,0,
                0,1,0,1,
                0,1,0,0,
                0,0,0,0,
                0,1,0,1,
                0,1,0,1,
                0,1,0,1,
                0,1,0,1,
            };
            Console.WriteLine(string.Join("", num2InAdcode));
            Console.WriteLine('\n');
            Console.WriteLine(Multiplication(num1InAdcode, num2InAdcode));
            Console.WriteLine(Convert.ToString(num1_in_decimal * num2_in_decimal));
        }
    }
}