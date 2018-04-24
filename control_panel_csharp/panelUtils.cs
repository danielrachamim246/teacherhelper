using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net.Sockets;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Threading;

namespace teacherhelper_control_panel
{
    class THNetworking
    {
        private TcpClient client;
        private byte[] buffer;
        public THNetworking()
        {
            // Default - Networking to the server mgmt service
            this.client = new TcpClient("127.0.0.1", 8003);
            this.buffer = new byte[100];
        }
        public THNetworking(String ip, int port)
        {
            this.client = new TcpClient(ip, port);
            this.buffer = new byte[100];
        }
        public THNetworking(int port)
        {
            // Default - Networking to localhost, choose your own port
            this.client = new TcpClient("127.0.0.1", port);
            this.buffer = new byte[100];
        }
        private String decodeAscii(byte[] buffer)
        {
            int count = Array.IndexOf<byte>(buffer, 0, 0);
            if (count < 0) count = buffer.Length;
            return Encoding.ASCII.GetString(buffer, 0, count);
        }
        public void sendPacket(String msg)
        {
            this.client.Client.Send(Encoding.ASCII.GetBytes(msg));
        }

        public byte[] getRecvBytes()
        {
            this.client.Client.Receive(this.buffer);
            return this.buffer;
        }

        public String getRecvString()
        {
            this.client.Client.Receive(this.buffer);
            return decodeAscii(this.buffer);
        }
    }

    class THControlPanel
    {
        private THNetworking cpNetworking;
        public THControlPanel()
        {
            this.cpNetworking = new THNetworking();
        }
        public String sendCommand(String cmd)
        {
            this.cpNetworking.sendPacket(cmd);
            return this.cpNetworking.getRecvString();
        }
    }

    static class THThreading
    {
        public static void autoRefreshThreadFunc(frmMain f)
        {
            // Infinite loop with i
            for(int i = 0; true; i++)
            {
                f.refresh(i);
                Thread.Sleep(1000);
            }
        }
        public static void startAutoRefresh(frmMain f)
        {
            var thread = new Thread(
                () => autoRefreshThreadFunc(f));
            thread.Start();
        }
    }

    static class Program
    {
        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new frmMain());
        }
    }
}
