import java.io.*;
import java.net.*;
import java.net.InetAddress;
import java.util.*;

public class ChatServer{
	int port = 9000;
	ServerSocket server;
	InputStream is;

	Vector<ServerThread> connectList;

	int cnt = 0;

	public ChatServer(){
		connectList = new Vector<ServerThread>();

		try{
			server = new ServerSocket(port);
			Socket client = new Socket();

			while(cnt != 10){
				client = server.accept();
				InetAddress inet = client.getInetAddress();
				String ip = inet.getHostAddress();
				System.out.println(ip + "join");

				ServerThread serverThread = new ServerThread(connectList, client);
				System.out.println("start");
				serverThread.start();

				connectList.add(serverThread);
				System.out.println("member : "+connectList.size());

				cnt++;

				
			}

			is = client.getInputStream();
			InputStreamReader reader;
			reader = new InputStreamReader(is);

			BufferedReader buffer = new BufferedReader(reader);

			OutputStream os = client.getOutputStream();
			OutputStreamWriter writer = new OutputStreamWriter(os);
			BufferedWriter bufferWriter = new BufferedWriter(writer);

			String data;
			while(true){
				data = buffer.readLine();
				System.out.println(data);
				bufferWriter.write(data+"\n");
				bufferWriter.flush();
			}
		} catch(IOException e){
			e.printStackTrace();
		}
	}

	public static void main(String[] args){
		new ChatServer();
	}
}
public class ServerThread extends Thread{
	Socket client;
	BufferedReader buffer;
	BufferedWriter bufferWriter;
	Vector<ServerThread> connectList;

	public ServerThread(Vector<ServerThread> connectList, Socket socket){
		this.connectList = connectList;
		this.client = socket;
		try{
			buffer = new BufferedReader(new InputStreamReader((client.getInputStream())));
			bufferWriter = new BufferedWriter(new OutputStreamWriter((client.getOutputStream())));
		}catch(IOException e){
			e.printStackTrace();
		}
	}

	public void run(){
		while(true){
			String msg = listen();
			send(msg);
		}
	}

	public String listen(){
		String msg = "";
		try{
			msg = buffer.readLine();
			System.out.println("msg : " + msg);
		} catch(IOException e){
			e.printStackTrace();
		}
		return msg;
	}

	public void send(String msg){
		try{
			for(int i = 0; i<connectList.size();i++){
				ServerThread st = connectList.get(i);

				st.bufferWriter.write(msg + "\n");
				st.bufferWriter.flush();
			}
		} catch(IOException e){
			e.printStackTrace();
		}
	}
}


