import java.io.File;
import java.io.IOException;

/**
 * @author 李文浩
 * @date 2018/9/30
 */
public class PhJs {
    //wkhtmltopdf.exe安装路径
    public static final String toPdfTool = "wkhtmltopdf";
    //需要生成PDF的URL
    public static final String srcPath = "http://www.jianshu.com/p/4d65857ffe5e";

    public static void main(String[] args) throws Exception {
        //设置纸张大小: A4, Letter, etc.
        String pageSize = "A4";
        //生成后存放路径
        String destPath = "/Users/liwenhao/Desktop/PDF生成教程及讲解.pdf";
        convert(pageSize, destPath);
    }

    public static void convert(String pageSize, String destPath) {
        File file = new File(destPath);
        File parent = file.getParentFile();
        if (!parent.exists()) {
            parent.mkdirs();
        }
        StringBuilder cmd = new StringBuilder();
        cmd.append(toPdfTool).append(" ");
        cmd.append("--page-size ");
        cmd.append(pageSize).append(" ");
        cmd.append(srcPath).append(" ");
        cmd.append(destPath);
        try {
            Runtime.getRuntime().exec(cmd.toString()).waitFor();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}
