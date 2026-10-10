# Past Work

Most of my career has been client and private work that can't be published. These are summaries, with no code or client data included. I'm happy to discuss any of them in more detail.

## Recent AI and tooling work

**Afrikaans speech recognition pipeline** · *2026*<br>
Desktop tool that downloads YouTube audio and auto-generated captions, lets reviewers correct caption timing in a GUI editor, and exports speech-recognition training datasets, with S3-compatible cloud sync for collaborating reviewers and a one-click Windows launcher. Companion scripts merge mixed-format speech datasets and fine-tune Whisper large-v3 for Afrikaans. [web-transcription](https://github.com/jeffvan302/web-transcription) is its web version.<br>
`Python` · `Whisper` · `Hugging Face Transformers` · `PyTorch` · `ffmpeg` · `S3`

**Real-time game combat overlay** · *2025–2026*<br>
C++ DirectX proxy DLL that draws an in-game overlay for Star Wars: The Old Republic: live combat-log parsing, per-second statistics, configurable alerts with audio, and an in-game layout editor. Plugins can be written in Python through an embedded interpreter with typed bindings. Built around a lock-free multi-producer queue, NTP-synchronised timestamps, per-thread CPU monitoring and a standalone DirectX 9 test harness.<br>
`C++` · `DirectX` · `Dear ImGui` · `Detours` · `pybind11` · `multithreading`

**Face recognition CLI** · *2026*<br>
Python command-line tool built on InsightFace embeddings. It enrolls people from labelled folders with automatic outlier rejection plus face quality and pose filtering, matches faces by cosine similarity with JSON output, and groups unknown faces under persistent IDs so they can be named later.<br>
`Python` · `InsightFace` · `OpenCV` · `NumPy`

**YOLOv8 toolkit for .NET** · *2024–2025*<br>
C# library for YOLOv8 ONNX inference (object detection and pose, on GPU or CPU) and dataset building, plus two desktop tools: one generates synthetic training images with noise and blur augmentation, the other organizes labelled images and exports train/validation sets with the YAML files Ultralytics training expects.<br>
`C#` · `.NET 8` · `ONNX Runtime` · `YOLOv8` · `WinForms`

## Business systems

**Case management and reporting platform** · *child and family services nonprofit · 2000–2020*<br>
Case management system I maintained for 20 years. I wrote about 60% of the original VB6 application and over the years reworked essentially every part of it. Later additions included a .NET Windows-service reporting engine that generates multi-threaded Excel reports on caseloads, case workers, billing and program activity, and SQL Server CLR triggers and stored procedures that keep case open/close state and program reports current inside the database.<br>
`VB6` · `VB.NET` · `SQL Server` · `SQL CLR` · `Windows services` · `Excel automation`

**Managed Windows fleet platform** · *same organization · 2019–2022*<br>
A Windows service, desktop companion app and admin web API used to provision and manage staff computers: scheduled tasks, software and printer deployment, firewall and group policy settings, BitLocker, VPN setup, certificate monitoring and Microsoft 365 (Graph and Exchange) integration. It also included a build pipeline that signs, versions and publishes each release.<br>
`C#` · `.NET Framework` · `Windows services` · `ASP.NET Web API` · `Microsoft Graph` · `EWS`

**Construction ERP reporting and integration** · *commercial contractor · 2017–2021*<br>
Reporting suite on top of the company's construction accounting ERP over ODBC: batch extraction of job status, project manager and change-order reports to Excel, filtered by job, salesperson, project manager and GL period. Also built an ERP data-access library, a job-linked timesheet application and a lightweight XML-backed table and index engine.<br>
`C#` · `ODBC` · `WinForms` · `Excel automation`

**Network Monitor** · *IT operations tool · 2015–2021*<br>
Map-based network monitoring desktop app: drag devices onto editable network maps and see live status from ping, SNMP (switch port statistics, printer toner), WMI service checks and SSH, with one-click RDP, SSH, VNC and web access plus a built-in OpenVPN connection manager.<br>
`VB.NET` · `SNMP` · `WMI` · `SSH` · `OpenVPN`

## Desktop utilities

**STO Keybinds** · *public desktop app · 2012–2018*<br>
Key-binding editor for the game Star Trek Online, with bind sets, presets, ground and space templates, guided help videos and a signed installer.<br>
`VB.NET` · `WinForms`

**Backup2Flash** · *2013–2016*<br>
Windows app and service that detects when a USB flash drive is plugged in, backs up chosen folders to it by copying only changed files, and ejects the drive when finished. Shipped with an MSI installer.<br>
`VB.NET` · `Windows services` · `Win32 device notifications`

---

[← Back to profile](https://github.com/jeffvan302)
