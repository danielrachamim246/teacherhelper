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

        }

        public void refresh(int c)
        {
            String clientString = this.cp.sendCommand("getClient");

            if (clientString == "None" && this.listClient.Items.Count == 0)
            {
                return;
            }

            String[] clientsArray = clientString.Split(',');

            if (c % 10 == 0)
            {
                for (int i = 0; i < this.listClient.Items.Count; i++)
                {
                    String client = (String) this.listClient.Items[i];
                    if (client.Contains("DISCONNECTED"))
                    {
                        this.listClient.Items.Remove(client);
                    }
                }
            }


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
                    if (listClientItem.Contains("DISCONNECTED"))
                        continue;

                    // TODO Delete shaming after a few times
                    MessageBox.Show("Client " + (String)this.listClient.Items[i] + " Disconnected!");
                    this.listClient.Items[i] = (String)this.listClient.Items[i] + " DISCONNECTED";
                }
            }


            // Add the new guys
            for (int i = 0; i < clientsArray.Length; i++)
            {
                if (clientsArray[i] == "None")
                {
                    continue;
                }
                if (!this.listClient.Items.Contains(clientsArray[i]))
                {
                    this.listClient.Items.Add(clientsArray[i]);
                }
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
    }
}
