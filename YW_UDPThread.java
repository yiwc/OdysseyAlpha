// bidirectional connection between client and server 
// secondary thread to the main file "TestingServer" 

package application;

import java.net.*;
import java.io.*;

public class YW_UDPThread extends Thread {
	protected DatagramSocket socket = null;
	protected String recvStr = new String();
	protected Boolean end = false;
	protected long LastAccess = System.currentTimeMillis();
	byte[] send_data = new byte[1024];
	protected DatagramPacket recvPacket;
	
	public boolean hasReceived = false;
		
	public String[] getString(){
		String[] jointStr;
		synchronized(this){
			jointStr = recvStr.split(" ");
			//System.out.printf("receive length data:%d\n" , jointStr.length);
			LastAccess = System.currentTimeMillis();
		}
		return jointStr;
	}
	
	public boolean sendMsg(String sendStr){
		boolean isSuccess = false;
		synchronized(this){
			send_data = sendStr.getBytes();
			DatagramPacket sendPacket = new DatagramPacket(send_data , send_data.length , recvPacket.getAddress() , recvPacket.getPort() );
	
			try {
				socket.send(sendPacket);
				//System.out.printf("sendStr=%s\n" ,sendStr);
				isSuccess = true;
			} catch (IOException e) {
	
				e.printStackTrace();
			}
		}
		return isSuccess;
	}
	
	public YW_UDPThread() throws IOException{
		this("UDPTestThread");
	}
	
	public YW_UDPThread(String name) throws IOException{
		super(name);
	  	
	}
	public void kill()
	{
		end = true;
	}

	public void dispose() {
		if(socket != null)
		{	
			if(!(socket.isClosed()))
				socket.close();
		}

		System.out.println("Disposing Client");
	} 


	public void run() {
		
		   byte[] recvBuf = new byte[2000];
		   // System.out.println("Start of UDPTestThread run()");
		   
		  	try {
		  		// Legal port
		  		socket = new DatagramSocket(30009);
		  		// Yuanrui's port
		  		// socket = new DatagramSocket(12358);
		  		socket.setSoTimeout(15000);
		    } catch (IOException ex) {
		          System.err.println("Can't setup server on this port number. ");
		          System.err.println(ex);
		    }		
		   
		   while( !end ){
			   recvPacket = new DatagramPacket(recvBuf , recvBuf.length);
				try{
					socket.receive(recvPacket);
					hasReceived = true;
					// System.out.println("FLAG: ");
					// System.out.println("getLocalPort: " +socket.getLocalPort() );
					// System.out.printf("getLocalAddress:%s\n" ,socket.getLocalAddress() );
					
				}catch(SocketTimeoutException e){
					System.out.println("Socket Timeout!");
					break;
				}
				catch(Exception e){
					System.out.println("Error! Closing Socket ");
					e.printStackTrace();
					break;
				}

				synchronized(this){
					recvStr = new String(recvPacket.getData() , 0 , recvPacket.getLength());
					//System.out.println("receive string:" + recvStr);
					
					if (System.currentTimeMillis()-LastAccess > 10000){
						break;
					}
				}
		   } // while
		   
			if(socket != null)
			{	
				if(!(socket.isClosed()))
				{
					socket.close();
				}
			}		   
		   System.out.println("Exiting Client");

	} // run 
} // class 