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

        private void timer1_Tick(object sender, EventArgs e)
        {
            // TEACHER ONLY
            // Set the picturebox size again
            this.pictureBox1.Size = this.Size;


            // Get Current Directory using time
            DateTime d = DateTime.Now;
            string dateStr = Convert.ToDateTime(d).ToString("yyyy-MM-dd");
            string hourStr = Convert.ToDateTime(d).ToString("HH");
            string minuteStr = Convert.ToDateTime(d).ToString("mm");
            string folderPath = "C:\\Users\\" + Environment.UserName + " \\snapshots\\" + this.userId + "\\" + dateStr + "\\" + hourStr + "\\" + minuteStr;
            
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
                //this.label1.Text += " not found!";
                this.pictureBox1.ImageLocation = this.lastWorkingImage;
                this.pictureBox1.Update();
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
            // Fullscreen
            this.WindowState = FormWindowState.Maximized;
            this.Bounds = Screen.PrimaryScreen.Bounds;

            // TEACHER ONLY
            //this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;        

            // Scretch the picturebox on all the form (fullscreen)
            this.pictureBox1.Size = this.Size;

            //MessageBox.Show("Streaming client " + this.userId.ToString());
        }
    }

}
