using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

internal static class Lanzador
{
    [STAThread]
    private static int Main()
    {
        try
        {
            string carpeta = AppDomain.CurrentDomain.BaseDirectory;
            string runtime = Path.Combine(carpeta, "runtime");
            string fuente = Path.Combine(carpeta, "Codigo fuente");
            string programa = Path.Combine(fuente, "main.py");
            var proceso = new ProcessStartInfo
            {
                FileName = Path.Combine(runtime, "pythonw.exe"),
                Arguments = "-B \"" + programa + "\"",
                WorkingDirectory = carpeta,
                UseShellExecute = false
            };
            proceso.EnvironmentVariables["TCL_LIBRARY"] = Path.Combine(runtime, "tcl", "tcl8.6");
            proceso.EnvironmentVariables["TK_LIBRARY"] = Path.Combine(runtime, "tcl", "tk8.6");

            using (Process ventana = Process.Start(proceso))
            {
                ventana.WaitForExit();
                if (ventana.ExitCode == 0)
                    return 0;
            }
            throw new InvalidOperationException("El simulador se cerro con un error.");
        }
        catch (Exception error)
        {
            MessageBox.Show(error.Message + "\nExtrae el ZIP completo y abre el ejecutable desde la carpeta extraida.",
                "Laboratorio Termico", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
    }
}
