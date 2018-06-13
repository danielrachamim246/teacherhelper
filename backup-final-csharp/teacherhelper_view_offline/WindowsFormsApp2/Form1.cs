using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;

namespace testing_Photo
{
    public partial class Form1 : Form
    {
        public int userId;
        UserPhotoData upd;
        string selectedDate = "";
        string selectedHour = "";
        string selectedMinute = "";

        int counter;
        int imageCounter;
        string folderPath;
        string lastWorkingImage;
        public Form1()
        {
            InitializeComponent();
            this.counter = 0;
            this.imageCounter = 0;
            this.folderPath = "";
            
            this.lastWorkingImage = "";
        }

        private void fillDates()
        {
            this.comboDate.Items.Clear();
            foreach (string iDate in this.upd.dates)
            {
                this.comboDate.Items.Add(iDate);
            }
        }

        private void fillHours(string dateStr)
        {
            // Find the index of the date in the array
            int iDate = -1;
            for (int i = 0; i < this.upd.dates.Length; i++)
            {
                if (this.upd.dates[i] == dateStr)
                {
                    iDate = i;
                    break;
                }
            }


            // Fill the hours
            this.comboHour.Items.Clear();
            foreach (string iHour in this.upd.hours[iDate])
            {
                this.comboHour.Items.Add(iHour);
            }
        }

        private void fillMinuets(string dateStr, string hourStr)
        {
            // Find the index of the date in the array
            int i = 0;
            int iDate = -1;
            for (i = 0; i < this.upd.dates.Length; i++)
            {
                if (this.upd.dates[i] == dateStr)
                {
                    iDate = i;
                    break;
                }
            }

            // Find the index of the hour
            int iHour = -1;
            for (i = 0; i < this.upd.hours.Length; i++)
            {
                if (this.upd.hours[iDate][i] == hourStr)
                {
                    iHour = i;
                    break;
                }
            }


            // Fill the minuets
            this.comboMinute.Items.Clear();
            foreach (string iMin in this.upd.minutes[iDate][iHour])
            {
                this.comboMinute.Items.Add(iMin);
            }
        }


        private void goToNextMinute()
        {
            int i = 0;
            int iDate = -1;
            for (i = 0; i < this.upd.dates.Length; i++)
            {
                if (this.upd.dates[i] == this.selectedDate)
                {
                    iDate = i;
                    break;
                }
            }

            // Find the index of the hour
            int iHour = -1;
            for (i = 0; i < this.upd.hours.Length; i++)
            {
                if (this.upd.hours[iDate][i] == this.selectedHour)
                {
                    iHour = i;
                    break;
                }
            }

            int[] intArray = new int[this.upd.minutes[iDate][iHour].Length];

            // Create the integer array
            for(i = 0; i < this.upd.minutes[iDate][iHour].Length; i++)
            {
                intArray[i] = int.Parse(this.upd.minutes[iDate][iHour][i]);
            }

            // Sort the array
            Array.Sort(intArray);

            // Find the next one
            for(i = 0; i < intArray.Length; i++)
            {
                if (intArray[i] == int.Parse(this.selectedMinute))
                {
                    if (i + 1 == intArray.Length)
                        break;
                    else
                    {
                        // Change the minute
                        this.selectedMinute = intArray[i + 1].ToString();
                        this.comboMinute.Text = this.selectedMinute;
                        return;
                    }

                }
            }
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            // TEACHER ONLY
            // Set the picturebox size again
            this.pictureBox1.Size = this.Size;

            // Get Current Directory using time
            // TODO GET SELECTION FROM UPD
            DateTime d = DateTime.Now;
            string dateStr = this.selectedDate;
            string hourStr = this.selectedHour;
            string minuteStr = this.selectedMinute;
            string folderPath = "C:\\Users\\user\\snapshots\\" + this.userId + "\\" + dateStr + "\\" + hourStr + "\\" + minuteStr;
            
            if (folderPath != this.folderPath)
            {
                // New folder, start from zero
                this.imageCounter = 0;
                this.folderPath = folderPath;
            }

            String fileName = this.folderPath + "\\" + this.imageCounter + ".jpg";
            //this.label1.Text = fileName;
            if (!File.Exists(fileName))
            {
                goToNextMinute();
            } else
            {
                this.pictureBox1.ImageLocation = fileName;
                this.lastWorkingImage = fileName;
                this.pictureBox1.Update();
                this.imageCounter++;
            }

            counter = (counter + 1) % 200;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            timer1.Enabled = false;

            // Fullscreen
            this.WindowState = FormWindowState.Normal;
            this.Bounds = Screen.PrimaryScreen.Bounds;

            // TEACHER ONLY
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;        

            // Scretch the picturebox on all the form (fullscreen)
            this.pictureBox1.Size = this.Size;

            // User ID
            this.Text = "View - Offline - Client " + this.userId.ToString();

            // Init data
            this.upd = new UserPhotoData(this.userId);
            fillDates();

            // Ready
            MessageBox.Show("Offline Streaming client " + this.userId.ToString());
        }

        private void btnRefresh_Click(object sender, EventArgs e)
        {
            this.upd = new UserPhotoData(this.userId);
            fillDates();
        }

        private void btnStop_Click(object sender, EventArgs e)
        {
            this.imageCounter = 0;
            timer1.Enabled = false;
        }

        private void btnRun_Click(object sender, EventArgs e)
        {
            // Take the arguments
            this.selectedDate = (string) this.comboDate.SelectedItem;
            this.selectedHour = (string)this.comboHour.SelectedItem;
            this.selectedMinute = (string)this.comboMinute.SelectedItem;

            // Start
            this.imageCounter = 0;
            timer1.Enabled = true;
        }

        private void comboDate_SelectedIndexChanged(object sender, EventArgs e)
        {
            string strDate = (string) this.comboDate.SelectedItem;
            fillHours(strDate);
            this.comboMinute.Items.Clear();
        }

        private void comboHour_SelectedIndexChanged(object sender, EventArgs e)
        {
            string strDate = (string)this.comboDate.SelectedItem;
            string strHour = (string)this.comboHour.SelectedItem;
            fillMinuets(strDate, strHour);
        }

        private void comboMinute_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }

}
