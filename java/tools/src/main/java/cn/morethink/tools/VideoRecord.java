package cn.morethink.tools;


import org.bytedeco.javacpp.avcodec;
import org.bytedeco.javacpp.avutil;
import org.bytedeco.javacpp.opencv_core;
import org.bytedeco.javacpp.opencv_core.IplImage;
import org.bytedeco.javacv.FFmpegFrameRecorder;
import org.bytedeco.javacv.FrameRecorder.Exception;
import org.bytedeco.javacv.OpenCVFrameConverter;

import javax.imageio.ImageIO;
import javax.sound.sampled.*;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.ShortBuffer;
import java.util.Scanner;
import java.util.concurrent.ScheduledThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import static org.bytedeco.javacpp.opencv_imgcodecs.cvLoadImage;

/**
 * 通过javacv实现录屏
 *
 * @author 李文浩
 * @date 2018/10/15
 */
public class VideoRecord {
    private ScheduledThreadPoolExecutor screenTimer;
    private final Rectangle rectangle = new Rectangle(1920, 1090);
    private FFmpegFrameRecorder recorder;
    private Robot robot;
    private OpenCVFrameConverter.ToIplImage conveter;
    private BufferedImage screenCapture;
    private final int AUDIO_DEVICE_INDEX = 4;
    private ScheduledThreadPoolExecutor exec;
    private TargetDataLine line;
    private AudioFormat audioFormat;
    private DataLine.Info dataLineInfo;
    private boolean isHaveDevice = true;
    private String fileName;
    private long startTime = 0;
    private long videoTS = 0;
    private long pauseTime = 0;
    private double frameRate = 5;

    public VideoRecord(String fileName, boolean isHaveDevice) {
        // TODO Auto-generated constructor stub
        recorder = new FFmpegFrameRecorder(fileName + ".mp4", 1920, 1090);
        // recorder.setVideoCodec(avcodec.AV_CODEC_ID_H264); // 28
        // recorder.setVideoCodec(avcodec.AV_CODEC_ID_FLV1); // 28
        recorder.setVideoCodec(avcodec.AV_CODEC_ID_MPEG4); // 13
        recorder.setFormat("mp4");
        // recorder.setFormat("mov,mp4,m4a,3gp,3g2,mj2,h264,ogg,MPEG4");
        recorder.setSampleRate(44100);
        recorder.setFrameRate(frameRate);

        recorder.setVideoQuality(0);
        recorder.setVideoOption("crf", "23");
        // 2000 kb/s, 720P视频的合理比特率范围
        recorder.setVideoBitrate(1000000);
        /**
         * 权衡quality(视频质量)和encode speed(编码速度) values(值)： ultrafast(终极快),superfast(超级快),
         * veryfast(非常快), faster(很快), fast(快), medium(中等), slow(慢), slower(很慢),
         * veryslow(非常慢)
         * ultrafast(终极快)提供最少的压缩（低编码器CPU）和最大的视频流大小；而veryslow(非常慢)提供最佳的压缩（高编码器CPU）的同时降低视频流的大小
         * 参考：https://trac.ffmpeg.org/wiki/Encode/H.264 官方原文参考：-preset ultrafast as the
         * name implies provides for the fastest possible encoding. If some tradeoff
         * between quality and encode speed, go for the speed. This might be needed if
         * you are going to be transcoding multiple streams on one machine.
         */
        recorder.setVideoOption("preset", "slow");
        recorder.setPixelFormat(avutil.AV_PIX_FMT_YUV420P); // yuv420p
        recorder.setAudioChannels(2);
        recorder.setAudioOption("crf", "0");
        // Highest quality
        recorder.setAudioQuality(0);
        recorder.setAudioCodec(avcodec.AV_CODEC_ID_AAC);
        try {
            robot = new Robot();
        } catch (AWTException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        try {
            recorder.start();
        } catch (Exception e) {
            // TODO Auto-generated catch block
            System.out.print("*******************************");
        }
        conveter = new OpenCVFrameConverter.ToIplImage();
        this.isHaveDevice = isHaveDevice;
        this.fileName = fileName;
    }

    public void start() {

        if (startTime == 0) {
            startTime = System.currentTimeMillis();
        }
        if (pauseTime == 0) {
            pauseTime = System.currentTimeMillis();
        }

        if (isHaveDevice) {
            new Thread(new Runnable() {

                @Override
                public void run() {
                    // TODO Auto-generated method stub
                    caputre();
                }
            }).start();

        }
        screenTimer = new ScheduledThreadPoolExecutor(1);
        screenTimer.scheduleAtFixedRate(new Runnable() {
            @Override
            public void run() {
                try {
                    screenCapture = robot.createScreenCapture(rectangle);
                    String name = fileName + ".JPEG";
                    File f = new File(name);
                    // 将screenshot对象写入图像文件
                    try {
                        ImageIO.write(screenCapture, "JPEG", f);
                    } catch (IOException e) {
                        // TODO Auto-generated catch block
                        e.printStackTrace();
                    }
                    // videoGraphics.drawImage(screenCapture, 0, 0, null);
                    IplImage image = cvLoadImage(name); // 非常吃内存！！
                    // 创建一个 timestamp用来写入帧中
                    videoTS = 1000 * (System.currentTimeMillis() - startTime - (System.currentTimeMillis() - pauseTime));
                    // 检查偏移量
                    if (videoTS > recorder.getTimestamp()) {
                        recorder.setTimestamp(videoTS);
                    }
                    recorder.record(conveter.convert(image));
                    opencv_core.cvReleaseImage(image);
                    f.delete();
                    System.gc();
                } catch (Exception ex) {
                    // ex.printStackTrace();
                }
            }
        }, (int) (1000 / frameRate), (int) (1000 / frameRate), TimeUnit.MILLISECONDS);

    }

    public void caputre() {
        audioFormat = new AudioFormat(44100.0F, 16, 2, true, false);
        dataLineInfo = new DataLine.Info(TargetDataLine.class, audioFormat);
        try {
            line = (TargetDataLine) AudioSystem.getLine(dataLineInfo);
        } catch (LineUnavailableException e1) {
            // TODO Auto-generated catch block
            System.out.println("#################");
        }
        try {
            line.open(audioFormat);
        } catch (LineUnavailableException e1) {
            // TODO Auto-generated catch block
            e1.printStackTrace();
        }
        line.start();

        int sampleRate = (int) audioFormat.getSampleRate();
        int numChannels = audioFormat.getChannels();

        int audioBufferSize = sampleRate * numChannels;
        byte[] audioBytes = new byte[audioBufferSize];

        exec = new ScheduledThreadPoolExecutor(1);
        exec.scheduleAtFixedRate(new Runnable() {
            @Override
            public void run() {
                try {
                    int nBytesRead = line.read(audioBytes, 0, line.available());
                    int nSamplesRead = nBytesRead / 2;
                    short[] samples = new short[nSamplesRead];

                    // Let's wrap our short[] into a ShortBuffer and
                    // pass it to recordSamples
                    ByteBuffer.wrap(audioBytes).order(ByteOrder.LITTLE_ENDIAN).asShortBuffer().get(samples);
                    ShortBuffer sBuff = ShortBuffer.wrap(samples, 0, nSamplesRead);

                    // recorder is instance of
                    // org.bytedeco.javacv.FFmpegFrameRecorder
                    recorder.recordSamples(sampleRate, numChannels, sBuff);
                    System.gc();
                } catch (org.bytedeco.javacv.FrameRecorder.Exception e) {
                    e.printStackTrace();
                }
            }
        }, (int) (1000 / frameRate), (int) (1000 / frameRate), TimeUnit.MILLISECONDS);
    }

    public void stop() {
        if (null != screenTimer) {
            screenTimer.shutdownNow();
        }
        try {
            recorder.stop();
            recorder.release();
            recorder.close();
            screenTimer = null;
            screenCapture = null;
            if (isHaveDevice) {
                if (null != exec) {
                    exec.shutdownNow();
                }
                if (null != line) {
                    line.stop();
                    line.close();
                }
                dataLineInfo = null;
                audioFormat = null;
            }
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

    }

    public void pause() throws Exception {
        screenTimer.shutdownNow();
        screenTimer = null;
        if (isHaveDevice) {
            exec.shutdownNow();
            exec = null;
            line.stop();
            line.close();
            dataLineInfo = null;
            audioFormat = null;
            line = null;
        }
        pauseTime = System.currentTimeMillis();
    }

    public static void main(String[] args) throws Exception, AWTException {
        VideoRecord videoRecord = new VideoRecord("/Users/liwenhao/Desktop/test", true);
        videoRecord.start();
        System.out.println("你要停止吗？请输入(stop)，程序会停止。");
        Scanner sc = new Scanner(System.in);
        if (sc.next().equalsIgnoreCase("stop")) {
            videoRecord.stop();
        }
        if (sc.next().equalsIgnoreCase("pause")) {
            videoRecord.pause();
        }
        if (sc.next().equalsIgnoreCase("start")) {
            videoRecord.start();
        }

    }

}

