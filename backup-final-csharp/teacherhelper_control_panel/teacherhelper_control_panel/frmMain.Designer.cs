namespace teacherhelper_control_panel
{
    partial class frmMain
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.listClient = new System.Windows.Forms.ListBox();
            this.btnSnapStart = new System.Windows.Forms.Button();
            this.btnSnapStop = new System.Windows.Forms.Button();
            this.btnLock = new System.Windows.Forms.Button();
            this.btnStreamLive = new System.Windows.Forms.Button();
            this.btnStreamOffline = new System.Windows.Forms.Button();
            this.btnExit = new System.Windows.Forms.Button();
            this.btnRefresh = new System.Windows.Forms.Button();
            this.btnUnlock = new System.Windows.Forms.Button();
            this.btnStartSharing = new System.Windows.Forms.Button();
            this.btnStopSharing = new System.Windows.Forms.Button();
            this.btnStartClientSharing = new System.Windows.Forms.Button();
            this.btnStopClientSharing = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.txtClientId = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.label1.Location = new System.Drawing.Point(200, 9);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(151, 48);
            this.label1.TabIndex = 0;
            this.label1.Text = "TeacherHelper\r\nControl Panel";
            // 
            // listClient
            // 
            this.listClient.FormattingEnabled = true;
            this.listClient.Location = new System.Drawing.Point(34, 78);
            this.listClient.Name = "listClient";
            this.listClient.SelectionMode = System.Windows.Forms.SelectionMode.MultiSimple;
            this.listClient.Size = new System.Drawing.Size(152, 264);
            this.listClient.TabIndex = 1;
            // 
            // btnSnapStart
            // 
            this.btnSnapStart.Location = new System.Drawing.Point(204, 78);
            this.btnSnapStart.Name = "btnSnapStart";
            this.btnSnapStart.Size = new System.Drawing.Size(156, 23);
            this.btnSnapStart.TabIndex = 2;
            this.btnSnapStart.Text = "Snapshot Start";
            this.btnSnapStart.UseVisualStyleBackColor = true;
            this.btnSnapStart.Click += new System.EventHandler(this.btnSnapStart_Click);
            // 
            // btnSnapStop
            // 
            this.btnSnapStop.Location = new System.Drawing.Point(366, 78);
            this.btnSnapStop.Name = "btnSnapStop";
            this.btnSnapStop.Size = new System.Drawing.Size(156, 23);
            this.btnSnapStop.TabIndex = 3;
            this.btnSnapStop.Text = "Snapshot Stop";
            this.btnSnapStop.UseVisualStyleBackColor = true;
            this.btnSnapStop.Click += new System.EventHandler(this.btnSnapStop_Click);
            // 
            // btnLock
            // 
            this.btnLock.Location = new System.Drawing.Point(204, 107);
            this.btnLock.Name = "btnLock";
            this.btnLock.Size = new System.Drawing.Size(156, 23);
            this.btnLock.TabIndex = 4;
            this.btnLock.Text = "lock";
            this.btnLock.UseVisualStyleBackColor = true;
            this.btnLock.Click += new System.EventHandler(this.btnLock_Click);
            // 
            // btnStreamLive
            // 
            this.btnStreamLive.Location = new System.Drawing.Point(204, 136);
            this.btnStreamLive.Name = "btnStreamLive";
            this.btnStreamLive.Size = new System.Drawing.Size(156, 23);
            this.btnStreamLive.TabIndex = 5;
            this.btnStreamLive.Text = "stream client - live";
            this.btnStreamLive.UseVisualStyleBackColor = true;
            this.btnStreamLive.Click += new System.EventHandler(this.btnStreamLive_Click);
            // 
            // btnStreamOffline
            // 
            this.btnStreamOffline.Location = new System.Drawing.Point(366, 136);
            this.btnStreamOffline.Name = "btnStreamOffline";
            this.btnStreamOffline.Size = new System.Drawing.Size(156, 23);
            this.btnStreamOffline.TabIndex = 6;
            this.btnStreamOffline.Text = "stream client - offline";
            this.btnStreamOffline.UseVisualStyleBackColor = true;
            this.btnStreamOffline.Click += new System.EventHandler(this.btnStreamOffline_Click);
            // 
            // btnExit
            // 
            this.btnExit.Location = new System.Drawing.Point(204, 319);
            this.btnExit.Name = "btnExit";
            this.btnExit.Size = new System.Drawing.Size(315, 23);
            this.btnExit.TabIndex = 7;
            this.btnExit.Text = "Exit";
            this.btnExit.UseVisualStyleBackColor = true;
            this.btnExit.Click += new System.EventHandler(this.btnExit_Click);
            // 
            // btnRefresh
            // 
            this.btnRefresh.Location = new System.Drawing.Point(204, 290);
            this.btnRefresh.Name = "btnRefresh";
            this.btnRefresh.Size = new System.Drawing.Size(315, 23);
            this.btnRefresh.TabIndex = 8;
            this.btnRefresh.Text = "Refresh List";
            this.btnRefresh.UseVisualStyleBackColor = true;
            this.btnRefresh.Click += new System.EventHandler(this.btnRefresh_Click);
            // 
            // btnUnlock
            // 
            this.btnUnlock.Location = new System.Drawing.Point(366, 107);
            this.btnUnlock.Name = "btnUnlock";
            this.btnUnlock.Size = new System.Drawing.Size(156, 23);
            this.btnUnlock.TabIndex = 9;
            this.btnUnlock.Text = "unlock";
            this.btnUnlock.UseVisualStyleBackColor = true;
            this.btnUnlock.Click += new System.EventHandler(this.btnUnlock_Click);
            // 
            // btnStartSharing
            // 
            this.btnStartSharing.Location = new System.Drawing.Point(204, 165);
            this.btnStartSharing.Name = "btnStartSharing";
            this.btnStartSharing.Size = new System.Drawing.Size(156, 23);
            this.btnStartSharing.TabIndex = 10;
            this.btnStartSharing.Text = "share teacher screen";
            this.btnStartSharing.UseVisualStyleBackColor = true;
            this.btnStartSharing.Click += new System.EventHandler(this.btnStartSharing_Click);
            // 
            // btnStopSharing
            // 
            this.btnStopSharing.Location = new System.Drawing.Point(366, 165);
            this.btnStopSharing.Name = "btnStopSharing";
            this.btnStopSharing.Size = new System.Drawing.Size(156, 23);
            this.btnStopSharing.TabIndex = 11;
            this.btnStopSharing.Text = "stop sharing teacher screen";
            this.btnStopSharing.UseVisualStyleBackColor = true;
            this.btnStopSharing.Click += new System.EventHandler(this.btnStopSharing_Click);
            // 
            // btnStartClientSharing
            // 
            this.btnStartClientSharing.Location = new System.Drawing.Point(204, 228);
            this.btnStartClientSharing.Name = "btnStartClientSharing";
            this.btnStartClientSharing.Size = new System.Drawing.Size(156, 23);
            this.btnStartClientSharing.TabIndex = 12;
            this.btnStartClientSharing.Text = "share client screen";
            this.btnStartClientSharing.UseVisualStyleBackColor = true;
            this.btnStartClientSharing.Click += new System.EventHandler(this.btnStartClientSharing_Click);
            // 
            // btnStopClientSharing
            // 
            this.btnStopClientSharing.Location = new System.Drawing.Point(366, 228);
            this.btnStopClientSharing.Name = "btnStopClientSharing";
            this.btnStopClientSharing.Size = new System.Drawing.Size(156, 23);
            this.btnStopClientSharing.TabIndex = 13;
            this.btnStopClientSharing.Text = "stop sharing client screen";
            this.btnStopClientSharing.UseVisualStyleBackColor = true;
            this.btnStopClientSharing.Click += new System.EventHandler(this.btnStopClientSharing_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(201, 207);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(118, 13);
            this.label2.TabIndex = 14;
            this.label2.Text = "Share Screen Client ID:";
            // 
            // txtClientId
            // 
            this.txtClientId.Location = new System.Drawing.Point(325, 204);
            this.txtClientId.Name = "txtClientId";
            this.txtClientId.Size = new System.Drawing.Size(100, 20);
            this.txtClientId.TabIndex = 15;
            // 
            // frmMain
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(531, 364);
            this.Controls.Add(this.txtClientId);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.btnStopClientSharing);
            this.Controls.Add(this.btnStartClientSharing);
            this.Controls.Add(this.btnStopSharing);
            this.Controls.Add(this.btnStartSharing);
            this.Controls.Add(this.btnUnlock);
            this.Controls.Add(this.btnRefresh);
            this.Controls.Add(this.btnExit);
            this.Controls.Add(this.btnStreamOffline);
            this.Controls.Add(this.btnStreamLive);
            this.Controls.Add(this.btnLock);
            this.Controls.Add(this.btnSnapStop);
            this.Controls.Add(this.btnSnapStart);
            this.Controls.Add(this.listClient);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "frmMain";
            this.Text = "TeacherHelper Control Panel";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.frmMain_FormClosing);
            this.Load += new System.EventHandler(this.frmMain_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ListBox listClient;
        private System.Windows.Forms.Button btnSnapStart;
        private System.Windows.Forms.Button btnSnapStop;
        private System.Windows.Forms.Button btnLock;
        private System.Windows.Forms.Button btnStreamLive;
        private System.Windows.Forms.Button btnStreamOffline;
        private System.Windows.Forms.Button btnExit;
        private System.Windows.Forms.Button btnRefresh;
        private System.Windows.Forms.Button btnUnlock;
        private System.Windows.Forms.Button btnStartSharing;
        private System.Windows.Forms.Button btnStopSharing;
        private System.Windows.Forms.Button btnStartClientSharing;
        private System.Windows.Forms.Button btnStopClientSharing;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox txtClientId;
    }
}

