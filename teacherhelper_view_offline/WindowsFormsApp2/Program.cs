using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace testing_Photo
{
    public class UserPhotoData
    {
        public int numOfDates;
        public string[] dates;
        public string[][] hours;
        public string[][][] minutes;
        public int[] minHour;
        public int[] maxHour;
        public int[][] minMinute;
        public int[][] maxMinute;
        
        public UserPhotoData(int userid)
        {
            string startPath = "C:\\Users\\user\\snapshots\\";
            startPath += userid.ToString();

            // Check if folder exists
            IEnumerable<String> dateDirs = Directory.EnumerateDirectories(startPath);
            this.numOfDates = dateDirs.Count();
            this.dates = new string[this.numOfDates];
            this.hours = new string[this.numOfDates][];
            this.minutes = new string[this.numOfDates][][];
            this.minHour = new int[this.numOfDates];
            this.maxHour = new int[this.numOfDates];
            this.minMinute = new int[this.numOfDates][];
            this.maxMinute = new int[this.numOfDates][];
            int i = 0;

            foreach (var dateDir in dateDirs)
            {
                this.dates[i] = Path.GetFileName(dateDir);
                IEnumerable<String> hourDirs = Directory.EnumerateDirectories(dateDir);
                int numOfHours = hourDirs.Count();
                this.hours[i] = new string[numOfHours];
                this.minutes[i] = new string[numOfHours][];
                this.minMinute[i] = new int[numOfHours];
                this.maxMinute[i] = new int[numOfHours];

                int minCurrentHour = -1;
                int maxCurrentHour = -1;
                foreach (var hourDir in hourDirs)
                {
                    string strHour = Path.GetFileName(hourDir);
                    if (minCurrentHour == -1 || maxCurrentHour == -1)
                    {
                        minCurrentHour = int.Parse(strHour);
                        maxCurrentHour = int.Parse(strHour);
                        continue;
                    }

                    if (int.Parse(strHour) < minCurrentHour)
                    {
                        minCurrentHour = int.Parse(strHour);
                    }

                    if (int.Parse(strHour) > maxCurrentHour)
                    {
                        maxCurrentHour = int.Parse(strHour);
                    }
                }

                this.minHour[i] = minCurrentHour;
                this.maxHour[i] = maxCurrentHour;

                // Now, for each hour
                int j = 0;
                foreach (var hourDir in hourDirs)
                {
                    this.hours[i][j] = Path.GetFileName(hourDir);
                    // Enumerate folders for each minute
                    IEnumerable<String> minDirs = Directory.EnumerateDirectories(hourDir);
                    int numOfMins = minDirs.Count();

                    this.minutes[i][j] = new string[numOfMins];
                    // For each minute, find the max and min
                    int minCurrentMin = -1;
                    int maxCurrentMin = -1;
                    int k = 0;
                    foreach (var minDir in minDirs)
                    {
                        string strMin = Path.GetFileName(minDir);
                        this.minutes[i][j][k] = strMin;
                        if (minCurrentMin == -1 || maxCurrentMin == -1)
                        { 
                            minCurrentMin = int.Parse(strMin);
                            maxCurrentMin = int.Parse(strMin);
                            k++;
                            continue;
                        }

                        if (int.Parse(strMin) < minCurrentMin)
                        {
                            minCurrentMin = int.Parse(strMin);
                        }

                        if (int.Parse(strMin) > maxCurrentMin)
                        {
                            maxCurrentMin = int.Parse(strMin);
                        }


                        k++;
                    }

                    this.minMinute[i][j] = minCurrentMin;
                    this.maxMinute[i][j] = maxCurrentMin;

                    j++;
                }

                i++;
            }
        }

    }
    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main(string[] args)
        {
            // Prase Arguments
            if (args.Length != 1)
            {
                return;
            }

            // Graphic
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Form1 f = new Form1();
            f.userId = int.Parse(args[0]);

            Application.Run(f);
        }
    }
}
