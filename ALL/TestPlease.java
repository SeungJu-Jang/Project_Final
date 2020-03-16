package testpack;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class TestPlease implements Runnable{
	   public static final int ServerPort = 9200;
	    public static final String ServerIP = "192.168.0.12";
	 
	    @Override
	    public void run() {
	 
	        try {
	            System.out.println("S: Connecting...");
	            ServerSocket serverSocket = new ServerSocket(ServerPort);
	 
	            while (true) {
	                Socket client = serverSocket.accept();
	                System.out.println("S: Receiving...");
	                try {
	                    BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
	                    String str = in.readLine();
	                    System.out.println("S: Received: '" + str + "'");
	            
	                     
	                    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(client.getOutputStream())), true);
	                    out.println("Server Received " + str);
	                } catch (Exception e) {
	                    System.out.println("S: Error");
	                    e.printStackTrace();
	                } finally {
	                    client.close();
	                    System.out.println("S: Done.");
	                }
	            }
	        } catch (Exception e) {
	            System.out.println("S: Error");
	            e.printStackTrace();
	        }
	    }
	 
	    public static void main(String[] args) {
			Thread desktopServerThread = new Thread(new TestPlease());
			desktopServerThread.start();
		}
}
