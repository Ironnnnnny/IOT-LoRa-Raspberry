package com.example.wifi_demo;

import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.Socket;
import java.nio.charset.StandardCharsets;

public class MainActivity extends AppCompatActivity {
    TextView info;
    TextView count_data;
    TextView recv_data;
    Button left;
    Button right;
    Button send;
    EditText et_send;
    ScrollView scrollView;
    int recv_count = 0;
    int send_count = 0;

    private String send_buff=null;
    private String recv_buff=null;
    private Handler handler = null;
    private Socket socket = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        findView();
        handler = new Handler();
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    socket = new Socket("192.168.12.1" , 7654);
                    System.out.println("###################");
                    if (socket!=null) {      //循环进行收发
                        recv();
                        while (true){
                            send();
                            System.out.println("recv1");
                            recv1();
                        }

                    }
                    else{
                        System.out.println("socket failed");
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();
    }


    private void findView() {
        info = (TextView) this.findViewById(R.id.info);
        recv_data = (TextView) this.findViewById(R.id.recv_data);
        count_data = (TextView) this.findViewById(R.id.count_data);
        left = (Button) this.findViewById(R.id.left);
        right = (Button) this.findViewById(R.id.right);
        send = (Button) this.findViewById(R.id.send);
        et_send = (EditText) this.findViewById(R.id.et_send);
        scrollView = (ScrollView) this.findViewById(R.id.scrollView);
    }

    private void recv() {
        //单开一个线程循环接收来自服务器端的消息
        System.out.println("recv void!!!!!");
        InputStream inputStream = null;
        try {
            inputStream = socket.getInputStream();
            System.out.println(inputStream+"123456789");
        } catch (IOException e) {
            e.printStackTrace();
        }catch (NullPointerException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        if (inputStream!=null){
            try {
                byte[] buffer = new byte[1024];
                int count = inputStream.read(buffer);//count是传输的字节数
                recv_buff = new String(buffer);
                recv_count++;//socket通信传输的是byte类型，需要转为String类型
                System.out.println("recv_buff: "+recv_buff);

            } catch (IOException e) {
                e.printStackTrace();
            }catch (NullPointerException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        //将受到的数据显示在TextView上
        if (recv_buff!=null){
            handler.post(runnableUi);
            handler.post(runnableRecv);
        }
    }


    private void recv1() {
        //单开一个线程循环接收来自服务器端的消息
        System.out.println("recv void!!!!!");
        InputStream inputStream = null;
        int count = 0;
        try {
            inputStream = socket.getInputStream();
            System.out.println(inputStream+"123456789");
        } catch (IOException e) {
            e.printStackTrace();
        }catch (NullPointerException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        if (inputStream!=null){
            try {
                byte[] buffer = new byte[1024];
                count = inputStream.read(buffer);//count是传输的字节数
                recv_buff = new String(buffer);
                recv_count++;//socket通信传输的是byte类型，需要转为String类型
                System.out.println("recv_buff: "+recv_buff);

            } catch (IOException e) {
                e.printStackTrace();
            }catch (NullPointerException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
        //将受到的数据显示在TextView上
        if (recv_buff!=null){
            handler.post(runnableData);
            handler.post(runnableRecv);
        }

        else if (count == 0) {
            handler.post(runnableDisconnect);
        }

    }

    //不能在子线程中刷新UI，应为textView是主线程建立的
    Runnable runnableUi = new Runnable() {
        @Override
        public void run() {
            try{
                info.setText(recv_buff);
            }catch (NullPointerException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }
    };

    Runnable runnableData = new Runnable() {
        @Override
        public void run() {
            try{
                scrollView.fullScroll(ScrollView.FOCUS_DOWN);
                recv_data.append(recv_buff+"\n");
//                count_data.setText("接收 "+recv_count+" 次, 发送 "+send_count+" 次");
            }catch (NullPointerException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }
    };

    Runnable runnableRecv = new Runnable() {
        @Override
        public void run() {
            try{
                count_data.setText("接收 "+recv_count+" 次, 发送 "+send_count+" 次");
            }catch (NullPointerException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }
    };

    Runnable runnableDisconnect = new Runnable() {
        @Override
        public void run() {
            try{
                info.setText("Disconnect");
            }catch (NullPointerException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }

        }
    };


    private void send() {
//        new Thread(new Runnable() {
//            @Override
//            public void run() {
//                while (true) {
//                    recv1();
//                }
//            }
//        }).start();

        send.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        send_buff = et_send.getText().toString();
                        OutputStream outputStream=null;
                        try {
                            outputStream = socket.getOutputStream();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }catch (NullPointerException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }

                        if(outputStream!=null){
                            try {
                                outputStream.write(send_buff.getBytes());
                                System.out.println("send_buff: " + send_buff);
                                outputStream.flush();
                                et_send.setText("");
                                handler.post(runnableRecv);

                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }

                    }
                }).start();
            }
        });

        left.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        send_buff = "left";
                        OutputStream outputStream = null;
                        try {
                            outputStream = socket.getOutputStream();
                        } catch (IOException e) {
                            e.printStackTrace();
                        } catch (NullPointerException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }

                        if (outputStream != null) {
                            try {
                                outputStream.write(send_buff.getBytes());
                                send_count++;
                                System.out.println("send_buff: " + send_buff);
                                handler.post(runnableRecv);
                                outputStream.flush();
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }

                    }
                }).start();
            }
        });

        right.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new Thread(new Runnable() {
                    @Override
                    public void run() {
                        send_buff = "right";
                        OutputStream outputStream = null;
                        try {
                            outputStream = socket.getOutputStream();
                        } catch (IOException e) {
                            e.printStackTrace();
                        } catch (NullPointerException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }

                        if (outputStream != null) {
                            try {
                                outputStream.write(send_buff.getBytes());
                                send_count++;
                                System.out.println("send_buff: " + send_buff);
                                outputStream.flush();
                                handler.post(runnableRecv);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }

                    }
                }).start();
            }
        });

    }

}