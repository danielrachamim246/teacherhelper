using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Threading;
using System.Diagnostics;
using System.IO;


namespace teacherhelper_control_panel
{
    public partial class frmMain : Form
    {
        private THControlPanel cp;
        public frmMain()
        {
            this.cp = new THControlPanel();
            InitializeComponent();
        }

        

        private void frmMain_Load(object sender, EventArgs e)
        {
            startTeacherSnapshot();
        }

        private void frmMain_FormClosing(object sender, FormClosingEventArgs e)
        {
            MessageBox.Show("Exiting, thanks!");
        }


        private void startTeacherSnapshot()
        {
            // TODO minimize the window
            ProcessStartInfo startInfo = new ProcessStartInfo();
            //startInfo.WorkingDirectory = "C:\\python27";
            startInfo.FileName = "cmd.exe";
            startInfo.CreateNoWindow = true;
            startInfo.UseShellExecute = false;
            startInfo.Arguments = "/c C:\\python27\\python.exe " + Directory.GetCurrentDirectory() + "\\client_teacher.py";
            Process.Start(startInfo);
        }

        public void refresh(int c)
        {
            String clientString = this.cp.sendCommand("getClient");

            if (clientString == "None")
            {
                this.listClient.Items.Clear();
                return;
            }

            String[] clientsArray = clientString.Split(',');


            for (int i = 0; i < this.listClient.Items.Count; i++)
            {
                bool found = false;
                for (int j = 0; j < clientsArray.Length; j++)
                {
                    String listClientItem = (String)this.listClient.Items[i];
                    if (listClientItem == clientsArray[j])
                    {
                        found = true;
                        break;
                    }
                }
                if (!found)
                {
                    // Disconnected
                    // Check if disconnected already
                    String listClientItem = (String)this.listClient.Items[i];
                    //if (listClientItem.Contains("DISCONNECTED"))
                    //    continue;

                    // TODO Delete shaming after a few times
                    MessageBox.Show("Client " + (String)this.listClient.Items[i] + " Disconnected!");
                    //this.listClient.Items[i] = (String)this.listClient.Items[i] + " DISCONNECTED";
                }
            }


            // Add the new guys
            this.listClient.Items.Clear();
            for (int i = 0; i < clientsArray.Length; i++)
            {
                if (clientsArray[i] == "None")
                {
                    break;
                }
                this.listClient.Items.Add(clientsArray[i]);
            }
        }

        private void btnRefresh_Click(object sender, EventArgs e)
        {
            //THThreading.startAutoRefresh(this);
            refresh(1);
        }

        private void btnExit_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void btnSnapStart_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("requestStreamClient," + (string)selecteditem);
            }
                
        }

        private void btnLock_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("lockClient," + (string)selecteditem);
            }
        }

        private void btnSnapStop_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("requestStopStreamClient," + (string)selecteditem);
            }
        }

        private void btnStreamLive_Click(object sender, EventArgs e)
        {
            if (this.listClient.SelectedItems.Count != 1)
            {
                MessageBox.Show("You CAN'T stream more than one client");
                return;
            }

            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.WorkingDirectory = Directory.GetCurrentDirectory();
                startInfo.FileName = "teacherhelper_teacher_view.exe";
                startInfo.Arguments = (string)selecteditem;
                Process.Start(startInfo);
            }
        }

        private void btnUnlock_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("unlockClient," + (string)selecteditem);
            }
        }

        private void btnStartSharing_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("getLiveStreamClient," + (string)selecteditem + ";0");
            }
        }

        private void btnStopSharing_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("stopLiveStreamClient," + (string)selecteditem);
            }
        }

        private void btnStreamOffline_Click(object sender, EventArgs e)
        {
            if (this.listClient.SelectedItems.Count != 1)
            {
                MessageBox.Show("You CAN'T stream more than one client");
                return;
            }

            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.WorkingDirectory = Directory.GetCurrentDirectory();
                startInfo.FileName = "teacherhelper_view_offline.exe";
                startInfo.Arguments = (string)selecteditem;
                Process.Start(startInfo);
            }
        }

        private void btnStartClientSharing_Click(object sender, EventArgs e)
        {
            try
            {
                int.Parse(txtClientId.Text);
            } catch(Exception)
            {
                MessageBox.Show("Cannot share the following client, invalid text!");
                return;
            }
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                if ((string)selecteditem == txtClientId.Text)
                {
                    // Client can't share his own screen to himself
                    continue;
                }
                this.cp.sendCommand("getLiveStreamClient," + (string)selecteditem + ";" + txtClientId.Text);
            }
        }

        private void btnStopClientSharing_Click(object sender, EventArgs e)
        {
            foreach (Object selecteditem in this.listClient.SelectedItems)
            {
                this.cp.sendCommand("stopLiveStreamClient," + (string)selecteditem);
            }
        }
    }
}
