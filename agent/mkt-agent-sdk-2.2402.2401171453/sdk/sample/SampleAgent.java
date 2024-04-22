package sample;

import java.util.Scanner;
import java.util.concurrent.atomic.AtomicBoolean;

import com.sas.mkt.agent.sdk.CI360Agent;
import com.sas.mkt.agent.sdk.CI360AgentException;
import com.sas.mkt.agent.sdk.CI360StreamInterface;
import com.sas.mkt.agent.sdk.ErrorCode;

/**
 * This class contains sample code used to demonstrate the usage of the CI360 Agent SDK 
 * {@link CI360Agent} to interact with CI360.   The sample will connect to the CI360 event stream
 * and will print out all events that arrive from CI360.   It also accepts a few command from standard
 * input.   
 * <br> <br>
 * exit - exits the sample agent
 * <br> <br>
 * send - sends an external event to CI360.   following the send command is the event to be injected.
 * The event is in JSON.  See {@link CI360Agent#injectEvent(String)}.
 * <br> <br>
 * bulk - requests a Signed S3 URL be returned for uploaded events into CI360.   Following the "bulk" command
 * is the application ID to use.   See {@link CI360Agent#requestBulkEventURL(String)}.
 * 
 * @author magibs
 *
 */
public class SampleAgent {
	static private AtomicBoolean alreadySeenStreamClosedCall = new AtomicBoolean(false);

	static boolean exiting=false;
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		try {
			final CI360Agent agent=new CI360Agent();
			CI360StreamInterface streamListener=new CI360StreamInterface() {
				public boolean processEvent(final String event) {
					Thread eventThread=new Thread() {
						public void run() {
							System.out.println("Event: " + event);
							if (event.startsWith("CFG")) {
								throw new RuntimeException("oops");
							}
						}
					};
					eventThread.start();
					return true;
				}

				public void streamClosed(ErrorCode errorCode, String message) {
					if (exiting) {
						System.out.println("Stream closed");
					} else {
						System.out.println("Stream closed " + errorCode + ": " + message);
				        if ((message!=null) && (
				        		message.contains("MKTCMN74224") ||   // incorrect JWT (bad format)
				        		message.contains("MKTCMN74248") ||   // tenant missing (unknown tenant.  maybe using wrong stack)
				        		message.contains("MKTCMN74261") ||   // invalid JWT (doesn't match any access points)
				        		message.contains("MKTCMN74265") ||   // agent out of date (version of API not supported by extapigw
				        		message.contains("MKTCMN74282")      // tenant is not licensed
				        		)) {
							System.exit(-1);
				    	}
						if (alreadySeenStreamClosedCall.compareAndSet(false, true)) {
							System.out.println("Passed compareAndSet test");
							try {
								Thread.sleep(15000);
							} catch (InterruptedException e) {

							}
		                	alreadySeenStreamClosedCall.set(false);
							try {
								//Try to reconnect to the event stream.
								agent.startStream(this, true);
							} catch (CI360AgentException e) {
								System.err.println("ERROR " + e.getErrorCode() + ": " + e.getMessage());
							}
						}
					}
				}
			};
			agent.startStream(streamListener, true);
			
			// Continue until user enters "exit" to standard input.
			Scanner in =new Scanner(System.in);
			while (true) {
				String input=in.nextLine();
				if (input.equalsIgnoreCase("exit")) {
					exiting=true;
					agent.stopStream();
					in.close();
					try {
						Thread.sleep(2000);
					} catch (InterruptedException e) {
						
					}
					System.exit(0);;				
				} else if (input.startsWith("send ")) {
					try {
						String message=agent.injectEvent(input.substring(5));
						System.out.println("SUCCESS: " + message);
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				} else if (input.startsWith("ping")) {
					try {
						String message=agent.ping();
						System.out.println("SUCCESS: " + message);
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				} else if (input.startsWith("config")) {
					try {
						String message=agent.getAgentConfig();
						System.out.println("SUCCESS: " + message);
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				} else if (input.startsWith("healthcheck")) {
					try {
						String message=agent.healthcheck();
						System.out.println("SUCCESS: " + message);
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				} else if (input.startsWith("connection")) {
					boolean status=agent.isConnected();
					System.out.println("Connection Status: " + (status?"UP":"DOWN"));
				} else if (input.startsWith("diag")) {
					try {
						String message=agent.diagnostics();
						System.out.println("SUCCESS: " + message);
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				} else if (input.startsWith("bulk ")) {
					try {
						String message=agent.requestBulkEventURL(input.substring(5));
						System.out.println("SUCCESS  URL: " + message);
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				} else if (input.startsWith("sendmessage ")) {
					try {
						agent.sendWebSocketMessage(input.substring(12).trim());
						System.out.println("SUCCESS: " + input.substring(12).trim());
					} catch (CI360AgentException e) {
						System.err.println("ERROR: " + e.getMessage());
					}
				}
			}
			
		} catch (CI360AgentException e) {
			System.out.println(e.getMessage());
			e.printStackTrace();
			System.exit(-1);
		}

	}

}
