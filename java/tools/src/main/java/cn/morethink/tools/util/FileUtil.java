package cn.morethink.tools.util;

import org.apache.commons.compress.archivers.tar.TarArchiveEntry;
import org.apache.commons.compress.archivers.tar.TarArchiveInputStream;
import org.apache.commons.compress.compressors.gzip.GzipCompressorInputStream;
import org.apache.commons.io.FileUtils;

import java.io.*;
import java.nio.MappedByteBuffer;
import java.nio.channels.Channels;
import java.nio.channels.FileChannel;
import java.nio.channels.ReadableByteChannel;
import java.nio.file.Paths;

import static cn.morethink.tools.util.ZipUtil.createDirectory;

/**
 * @author 李文浩
 * @date 2018/8/4
 */
public class FileUtil {


    /**
     * 解压 tar.gz 文件
     *
     * @param file      要解压的tar.gz文件对象
     * @param outputDir 要解压到某个指定的目录下
     * @throws IOException
     */
    public static void decompressTarGz2(File file, String outputDir) throws IOException {
        try (TarArchiveInputStream tarIn = new TarArchiveInputStream(
                new GzipCompressorInputStream(
                        new FileInputStream(file)))) {
            //创建输出目录
            createDirectory(outputDir, null);
            TarArchiveEntry entry = null;
            ReadableByteChannel inChannel = Channels.newChannel(tarIn);
            while ((entry = tarIn.getNextTarEntry()) != null) {
                //是目录
                if (entry.isDirectory()) {
                    //创建空目录
                    createDirectory(outputDir, entry.getName());
                } else {
                    //是文件
                    try (FileChannel out = new RandomAccessFile(Paths.get(outputDir + File.separator + entry.getName()).toFile(), "rw").getChannel()) {
                        out.transferFrom(inChannel, 0, entry.getSize());
                    }
                }

            }
        }
    }

    public static void nioTransferCopy(File source, File target) throws IOException {
        try (FileChannel in = new FileInputStream(source).getChannel()) {
            try (FileChannel out = new FileOutputStream(target).getChannel()) {
                in.transferTo(0, in.size(), out);
                //ByteBuffer buffer = ByteBuffer.allocate(1024 * 100);
                //int len = in.read(buffer);
                //while (len != -1) {
                //    // 反转缓冲区，即将读取开始下标设置为0
                //    buffer.flip();
                //    // 将数据写入到输出通道
                //    out.write(buffer);
                //    // 将缓冲区清空
                //    buffer.clear();
                //    len = in.read(buffer);
                //}
                //ByteBuffer buffer = ByteBuffer.allocateDirect(1024);
                //while (in.read(buffer) != -1) {
                //    buffer.flip();
                //    while (buffer.hasRemaining()) {
                //        out.write(buffer);
                //    }
                //    buffer.clear();
                //}
            }
        }
    }

    public static void nioCopy2(File source, File target) throws IOException {
        try (FileChannel in = new FileInputStream(source).getChannel()) {
            try (FileChannel out = new FileOutputStream(target).getChannel()) {
                MappedByteBuffer mbb = in.map(FileChannel.MapMode.READ_ONLY, 0, in.size());
                out.write(mbb);
            }
        }


    }

    public static void writeFile(InputStream in, OutputStream out) throws IOException {
        int length;
        byte[] b = new byte[1024 * 100];
        while ((length = in.read(b)) != -1) {
            out.write(b, 0, length);
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException {
        //File input = new File("/Users/liwenhao/Desktop/test/csv/xj_restaurant_id.csv");
        File input = new File("/Users/liwenhao/Desktop/test/csv/xj_restaurant_id.csv");
        File output1 = new File("/Users/liwenhao/Desktop/xj_restaurant_id-1.csv");
        File output2 = new File("/Users/liwenhao/Desktop/xj_restaurant_id-2.csv");
        FileUtils.deleteQuietly(output1);
        FileUtils.deleteQuietly(output2);
        long start = System.currentTimeMillis();
        //nioTransferCopy(input, output1);
        //System.out.println("time is " + (System.currentTimeMillis() - start) + "ms");
        //
        //Thread.sleep(2000);


        start = System.currentTimeMillis();
        try (InputStream fis = new FileInputStream(input)) {
            try (OutputStream fos = new FileOutputStream(output2)) {
                writeFile(fis, fos);
            }
        }
        System.out.println("time is " + (System.currentTimeMillis() - start) + "ms");
    }
}
