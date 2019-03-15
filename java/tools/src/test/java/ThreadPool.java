import lombok.Getter;
import lombok.Setter;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicLong;

/**
 * @author 李文浩
 * @date 2018/9/12
 */
public class ThreadPool {
    public static void main(String[] args) throws IOException, InterruptedException {
        Semaphore semaphore = new Semaphore(4);
        semaphore.acquire();
        //
        semaphore.release();
        //Executors.newSingleThreadExecutor();
        //new ThreadPoolExecutor(2, 10, 60, TimeUnit.SECONDS, new ArrayBlockingQueue<>(10));
        //BlockingQueue blockingQueue = new LinkedBlockingQueue(10);
        int count = 30;
        CountDownLatch countDownLatch = new CountDownLatch(count);
        AtomicLong atomicLong = new AtomicLong();
        //LongAdder atomicLong = new LongAdder();
        long start = System.currentTimeMillis();
        for (int i = 0; i < count; i++) {
            new Thread(new Runnable() {
                @Override
                public void run() {
                    while (System.currentTimeMillis() - start < 5000) {
                        atomicLong.incrementAndGet();
                        //atomicLong.increment();
                    }
                    countDownLatch.countDown();
                }
            }).start();

        }
        countDownLatch.await();
//319363724 302118374 178073806 193228265
        System.out.println(atomicLong.longValue());
        LinkedTransferQueue linkedTransferQueue;
        ThreadPoolExecutor threadPoolExecutor;
        ScheduledThreadPoolExecutor scheduledThreadPoolExecutor;
        LinkedBlockingQueue linkedBlockingQueue;
        ExecutorService service = Executors.newCachedThreadPool();
        List<Runnable> list = service.shutdownNow();
        list.forEach(runnable -> {
            Task task = (Task) runnable;
            if ("label1".equals(task.getLabel())) {
                task.setClosed(true);
            }
        });

    }

    @Getter
    @Setter
    static class Task implements Runnable {

        private boolean closed;

        private String label;

        @Override
        public void run() {

        }
    }

}
