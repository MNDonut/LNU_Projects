using System;

namespace Programs
{
    class Program
    {
        static void func(int n){
            double num_for_print = 0;
            for(double i = Math.Pow(10, n-1); i < Math.Pow(10, n); i++){
                num_for_print = i;
                char[] digits = i.ToString().ToCharArray();
                double[] num = new double[digits.Length];
                double[] sorted = new double[num.Length];
                for(int j = 0; j < num.Length; j++){
                    num[j] = Convert.ToInt32(digits[j]);
                    sorted[j] = num[j];
                }
                Array.Sort(sorted);
                for(int k = 0; k < sorted.Length; k++){
                    if(sorted[k] == num[k]){
                        if(k == sorted.Length - 1){
                            Console.WriteLine(num_for_print);
                        }
                        continue;
                    }
                    break;
                }
            }
        }
        static void Main(string[] args)
        {
            Console.Write("Write n: ");
            int n = Convert.ToInt32(Console.ReadLine());
            func(n);
        }
    }
}
