using System;
using System.Collections.Generic;
using System.Linq;

namespace ABC
{
    public static class Extensions
    {
        public static List<int> ExpandBegin(this IEnumerable<int> list, int discharge, int value = 0)
        {
            var expandedList = GenerateList(discharge, value).ToList();
            expandedList.AddRange(list);
            return expandedList;
        }
        
        public static IEnumerable<int> ExpandEnd(this IEnumerable<int> list, int discharge, int value = 0)
        {
            var expandedList = new List<int>(list);
            expandedList.AddRange(GenerateList(discharge, value));
            return expandedList;
        }

        public static bool Compare(this IEnumerable<int> thisEnumerable, IEnumerable<int> enumerable)
        {
            var ints = thisEnumerable.ToArray();
            var second = enumerable.ToArray();
            
            var result = ints.Union(second).Where(w => !(ints.Contains(w) && second.Contains(w)));
            return !result.Any();
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