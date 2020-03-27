using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace ABC
{
    public class Bin
    {
        public IEnumerable<int> ValueBin { get; private set; }
        public bool IsNegative { get; private set; }
        
        public Bin(double num)
        {
            IsNegative = num < 0;
            ValueBin = ToDirectCode(Math.Abs(num));
            if (IsNegative)
            {
                ValueBin = ToComplementCode();
            }
        }

        public Bin(IEnumerable<int> val)
        {
            ValueBin = val;
        }

        public Bin(IEnumerable<int> valueBin, bool isNegative = false)
        {
            ValueBin = valueBin;
            IsNegative = isNegative;
        }
        
        private static IEnumerable<int> ToDirectCode(double num)
        {
            var binary = new List<int>();
            while (num >= 1)
            {
                num /= 2;
                binary.Insert(0, num > Math.Truncate(num) ? 1 : 0);
                num = Math.Truncate(num);
            }

            if(binary.Count == 0) binary.Add(0);
            return binary;
        }

        private static IEnumerable<int> ToInvertCode(IList<int> bin)
        {
            for (var i = 0; i < bin.Count; i++)
            {
                bin[i] = bin[i] == 1 ? 0 : 1;
            }

            return bin;
        }

        private IEnumerable<int> ToComplementCode()
        {
            var bin = ToInvertCode(ValueBin.ToList());
            var res = new Bin(bin, IsNegative) + new Bin(1);
            
            return res.ValueBin;
        }

        private static IEnumerable<int> CalculateSum(IList<int> list1, IList<int> list2)
        {
            var addToNext = 0;
            for (var i = list1.Count - 1; i >= 0; i--)
            {
                list1[i] = Add(list1[i] += list2[i] + addToNext, out var add);
                addToNext = add;
            }

            if (addToNext != 0)
            {
                list1.Insert(0, addToNext);
            }
            
            return list1;
        }
        
        private static int Add(int binItem, out int add)
        {
            add = 0;
            if (binItem >= 2)
            {
                binItem -= 2;
                add = 1;
            }

            return binItem;
        }
        
        public static Bin operator +(Bin bin1, Bin bin2)
        {
            var (item1, item2) = Prepare(bin1, bin2);
            var add = CalculateSum(item1, item2);
            
            return new Bin(add);
        }

        public static Bin operator *(Bin bin1, Bin bin2)
        {
            var item1 = bin1.ValueBin.ToList();
            var item2 = bin2.ValueBin.ToList();
            var res = new Bin(0);
            var shift = 0;
            item2.Reverse();
            
            var items = new List<Bin>();

            foreach (var i in item2)
            {
                if (i != 0)
                {
                    var shifted = item1.ExpandEnd(shift);
                    res += new Bin(shifted);
                    items.Add(new Bin(shifted));
                }
                shift++;
            }
            
            var asd = new Bin(0);
            foreach (var bin in items)
            {
                asd += bin;
            }
            
            
            res.IsNegative = bin1.IsNegative != bin2.IsNegative;
            return res;
        }
        
        private static (List<int> item1, List<int> item2) Prepare(Bin bin1, Bin bin2)
        {
            var binVal1 = bin1.ValueBin.ToList();
            var binVal2 = bin2.ValueBin.ToList();

            var dif = binVal1.Count - binVal2.Count;
            for (var i = 0; i < dif; i++)
            {
                if (dif > 0) binVal2.Insert(0, bin2.IsNegative ? 1 : 0);
                if (dif < 0) binVal1.Insert(0, bin1.IsNegative ? 1 : 0);
            }

            return (binVal1, binVal2);
        }

        public IEnumerable<int> ComplementToDirect => IsNegative switch
        {
            true => ToInvertCode((this + new Bin(-1)).ValueBin.ToList()),
            _ => ValueBin
        };
        
        public double ToDouble()
        {
            var res = 0d;
            var bin = ComplementToDirect;
            var enumerable = bin as int[] ?? bin.ToArray();
         
            var pow = enumerable.Length - 1;
            foreach (var i in enumerable)
            {
                res += i * Math.Pow(2, pow);
                pow--;
            }

            return IsNegative ? -res : res;
        }
        
        public override string ToString()
        {
            return Regex.Replace(string.Join("", ValueBin), ".{4}", "$0 ");
        }
    }
}