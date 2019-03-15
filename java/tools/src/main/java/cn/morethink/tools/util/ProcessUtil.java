package cn.morethink.tools.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * @author 李文浩
 * @date 2018/10/23
 */
public class ProcessUtil {
    public static void main(String[] args) throws IOException, InterruptedException {
        Process process = Runtime.getRuntime().exec("ls -lh", null, new File("/"));
        BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream()));
        String inRes;
        StringBuilder inBuf = new StringBuilder();
        while ((inRes = in.readLine()) != null) {
            inBuf.append(inRes + "\n");
        }
        in.close();
        System.out.println(inBuf.toString());
    }
}
