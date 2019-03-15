package cn.morethink.nettyexample;

import cn.morethink.nettyexample.handler.NettyServerInitializer;
import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelOption;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.logging.LogLevel;
import io.netty.handler.logging.LoggingHandler;
import lombok.extern.slf4j.Slf4j;

import java.net.InetAddress;

/**
 * @author 李文浩
 * @date 2018/9/5
 */
@Slf4j
public final class NettyServer {

    public static final int PORT = 9999;

    public static void main(String[] args) throws Exception {
        EventLoopGroup boss = new NioEventLoopGroup(1);
        ServerBootstrap b = new ServerBootstrap();
        b.option(ChannelOption.SO_BACKLOG, 1024);
        b.group(boss)
                .channel(NioServerSocketChannel.class)
                .handler(new LoggingHandler(LogLevel.INFO))
                //传递路由类
                .childHandler(new NettyServerInitializer());

        Channel ch = b.bind(PORT).sync().channel();
        log.info("http://{}:{}/ start", InetAddress.getLocalHost().getHostAddress(), PORT);
        ch.closeFuture().sync();

    }

}
