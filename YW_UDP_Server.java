package application;

import java.io.IOException; // <--
import java.util.Arrays;    // <--
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.concurrent.TimeUnit;


import com.kuka.generated.ioAccess.RobotiqGrip3IOGroup; // <--

// Default
import com.kuka.roboticsAPI.applicationModel.RoboticsAPIApplication; // <--
import static com.kuka.roboticsAPI.motionModel.BasicMotions.*;       // <--
import com.kuka.roboticsAPI.controllerModel.Controller;              // <--
import com.kuka.roboticsAPI.deviceModel.LBR;                         // <--


import com.kuka.common.ThreadUtil;                                   // <--

import com.kuka.roboticsAPI.geometricModel.CartDOF;                  // <--
import com.kuka.roboticsAPI.geometricModel.Frame;                    // <--

import com.kuka.roboticsAPI.geometricModel.Tool;                     // <--

import com.kuka.roboticsAPI.geometricModel.World;                    // <--
import com.kuka.roboticsAPI.geometricModel.math.CoordinateAxis;
import com.kuka.roboticsAPI.geometricModel.redundancy.IRedundancyCollection;
import com.kuka.roboticsAPI.motionModel.IMotionContainer;
import com.kuka.roboticsAPI.motionModel.ISmartServoRuntime;       // <--

import com.kuka.roboticsAPI.motionModel.SmartServo;               // <--
import com.kuka.roboticsAPI.motionModel.controlModeModel.CartesianImpedanceControlMode; // <--
import com.kuka.roboticsAPI.sensorModel.ForceSensorData;             // <--
import com.kuka.roboticsAPI.userInterface.ServoMotionUtilities;   // <--

/**
 * Implementation of a robot application.
 * <p>
 * The application provides a {@link RoboticsAPITask#initialize()} and a 
 * {@link RoboticsAPITask#run()} method, which will be called successively in 
 * the application lifecycle. The application will terminate automatically after 
 * the {@link RoboticsAPITask#run()} method has finished or after stopping the 
 * task. The {@link RoboticsAPITask#dispose()} method will be called, even if an 
 * exception is thrown during initialization or run. 
 * <p>
 * <b>It is imperative to call <code>super.dispose()</code> when overriding the 
 * {@link RoboticsAPITask#dispose()} method.</b> 
 * 
 * @see #initialize()
 * @see #run()
 * @see #dispose()
 */

public class YW_UDP_Server extends RoboticsAPIApplication
{
	private Controller kuka_Sunrise_Cabinet_1; 
	private Tool ToolGripper;
	private RobotiqGrip3IOGroup FingerTip;
	private LBR lbr_iiwa_14_R820_1;
	private CartesianImpedanceControlMode mode = null ; 
	private CartesianImpedanceControlMode modeHandShake = null ;
	private YW_UDPThread client = null; // thread

	byte[] receive_data = new byte[1024];
	byte[] send_data = new byte[1024]; 

	boolean done=false;
	boolean _IsRunning = true;
	Frame initFrame = new Frame();
	int robotPosition=0; 
	int fingerTipForce=0; 
	double[] jointAngle = new double[8];

	enum p_mode {free, centering};
	p_mode previousMode = p_mode.centering; 

	double RB1_x = 0.0 ;
	double RB1_y = 0.0 ;
	double RB1_z = 0.0;
	double RB1_oa = 0.0 ;
	double RB1_ob = 0.0 ;
	double RB1_og = 0.0 ;
	double RB1_qx = 0.0 ;
	double RB1_qy = 0.0 ;
	double RB1_qz = 0.0 ;
	double RB1_qw = 0.0 ;
	double Old_RB1_x = 0.0 ;
	double Old_RB1_y = 0.0 ;
	double Old_RB1_z = 0.0 ;
	double Old_RB1_oa = 0.0 ;
	double Old_RB1_ob = 0.0 ;
	double Old_RB1_og = 0.0 ;
	double Old_RB1_qx = 0.0 ;
	double Old_RB1_qy = 0.0 ;
	double Old_RB1_qz = 0.0 ;
	double Old_RB1_qw = 0.0 ;
	double Old_Frame_x = 0.0 ;
	double Old_Frame_y = 0.0 ;
	double Old_Frame_z = 0.0 ;
	double Old_Frame_oa = 0.0 ;
	double Old_Frame_ob = 0.0 ;
	double Old_Frame_og = 0.0 ;
	double Org_X = 0.0; 
	double Org_Y = 0.0; 
	double Org_Z = 0.0; 
	double Org_a = 0.0; 
	double Org_b = 0.0; 
	double Org_g = 0.0; 
	
	// Pinching mode
	int gripper_mode = 11;
	// Original
	// int gripper_mode = 9;

	public void initialize()
	{
		lbr_iiwa_14_R820_1 = ServoMotionUtilities.locateLBR(getContext());

		kuka_Sunrise_Cabinet_1 = (Controller) getContext().getControllers().toArray()[0];

		FingerTip= new RobotiqGrip3IOGroup(kuka_Sunrise_Cabinet_1);

		ToolGripper=getApplicationData().createFromTemplate("ToolGripper");	

		mode = new CartesianImpedanceControlMode() ; //cyw original 20 20 20
		mode.parametrize(CartDOF.A).setStiffness(300);  	// rotation about Z
		mode.parametrize(CartDOF.B).setStiffness(300);		// rotation about Y
		mode.parametrize(CartDOF.C).setStiffness(300);		// rotation about X
		// Original
		// mode.parametrize(CartDOF.A).setStiffness(10) ;  	// rotation about Z
		// mode.parametrize(CartDOF.B).setStiffness(10);		// rotation about Y
		// mode.parametrize(CartDOF.C).setStiffness(10);		// rotation about X
		
		// Increase stiffness (reduce compliance)
		mode.parametrize(CartDOF.X).setStiffness(2000) ;//cyw original 300 300 300
		mode.parametrize(CartDOF.Y).setStiffness(2000) ;
		mode.parametrize(CartDOF.Z).setStiffness(2000) ;
		// Original
		// mode.parametrize(CartDOF.X).setStiffness(100) ;
		// mode.parametrize(CartDOF.Y).setStiffness(100) ;
		// mode.parametrize(CartDOF.Z).setStiffness(100) ;
		
		mode.parametrize(CartDOF.ALL).setDamping(0.7) ;

		modeHandShake = new CartesianImpedanceControlMode() ; //cyw original 50 50 10 1000 1000 1000
		modeHandShake.parametrize(CartDOF.A).setStiffness(300) ;  	// rotation about Z
		modeHandShake.parametrize(CartDOF.B).setStiffness(300);		// rotation about Y
		modeHandShake.parametrize(CartDOF.C).setStiffness(300);		// rotation about X

		modeHandShake.parametrize(CartDOF.X).setStiffness(2000) ;
		modeHandShake.parametrize(CartDOF.Y).setStiffness(2000) ;
		modeHandShake.parametrize(CartDOF.Z).setStiffness(2000) ;		
		modeHandShake.parametrize(CartDOF.ALL).setDamping(0.7) ;

		System.out.println("Initialized (Pick and Place - Amplified 1.5, translation only, with translational force feedback)" );
	} // initialise

	@Override 
	public void dispose()
	{
		_IsRunning = false ; 
		System.out.println(" Closing Sockets in Dispose Block"); 

		if(client != null)
			client.kill();

		super.dispose();
	} // dispose

	private void moveToInitialPositionNegativeZ()
	{	
		// Start From Better Initial Pose FIX
		// Lowered pinching pose (Demo)
		lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-20.13), Math.toRadians(31.34), Math.toRadians(0.06), Math.toRadians(-94.72) , Math.toRadians(-93.82), Math.toRadians(-57.79), Math.toRadians(-61.09)).setJointVelocityRel(0.3));
		
		// (4th try, a bit too far back the x-axis, it can jam A4)
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-21.34), Math.toRadians(28.10), Math.toRadians(0.06), Math.toRadians(-101.19) , Math.toRadians(-93.21), Math.toRadians(-58.64), Math.toRadians(-63.64)).setJointVelocityRel(0.3));
		// (3rd try, still at risk of jamming, but there's room in A4 to pull back in the x-axis)
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-17.89), Math.toRadians(38.52), Math.toRadians(0.06), Math.toRadians(-83.37) , Math.toRadians(-96.04), Math.toRadians(-56.43), Math.toRadians(-54.65)).setJointVelocityRel(0.3));
		// (2nd try, too low in z-axis, can crash into box, at risk of jamming)
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-17.89), Math.toRadians(47.65), Math.toRadians(0.04), Math.toRadians(-86.75) , Math.toRadians(-88.34), Math.toRadians(-55.99), Math.toRadians(-68.44)).setJointVelocityRel(0.3));
		// (1st try, too far back x-axis and too far up z-axis) 
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-19.84), Math.toRadians(37.05), Math.toRadians(-0.01), Math.toRadians(-98.11) , Math.toRadians(-89.86), Math.toRadians(-57.38), Math.toRadians(-79.66)).setJointVelocityRel(0.3));
		
		// Pinching pose
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-22.33), Math.toRadians(19.56), Math.toRadians(0.0), Math.toRadians(-85.61) , Math.toRadians(-108.45), Math.toRadians(-64.76), Math.toRadians(-44.78)).setJointVelocityRel(0.3));
		// Gimbal lock free pose
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-21.19), Math.toRadians(36.36), Math.toRadians(0.0), Math.toRadians(-79.12) , Math.toRadians(-81.02), Math.toRadians(-70.86), Math.toRadians(-63.43)).setJointVelocityRel(0.3));
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-21.19), Math.toRadians(36.36), Math.toRadians(0.0), Math.toRadians(-79.12) , Math.toRadians(-81.02), Math.toRadians(-70.86), Math.toRadians(28.29)).setJointVelocityRel(0.3));
		// Vetra pose
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-0.0), Math.toRadians(30.0), Math.toRadians(0.0), Math.toRadians(-90.0) , Math.toRadians(-0.0), Math.toRadians(-30.0), Math.toRadians(-35.0)).setJointVelocityRel(0.3));
		// Original
		// lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-0.0), Math.toRadians(30.0), Math.toRadians(0.0), Math.toRadians(-60.0) , Math.toRadians(-0.0), Math.toRadians(60.0), Math.toRadians(0.0)).setJointVelocityRel(0.3));

		if (FingerTip.getActReq() != gripper_mode)
		{
			FingerTip.setActReq(gripper_mode);
		}
		FingerTip.setSpeed(255);
		FingerTip.setForce(5);
		FingerTip.setPosReq(255); // close the gripper
		ThreadUtil.milliSleep(2000); 

	} 
	
	
	private void moveToInitialPositionPositiveY()
	{
		lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(30.0), Math.toRadians(90.0), Math.toRadians(0.0), Math.toRadians(-60.0) , Math.toRadians(-60.0), Math.toRadians(105.0), Math.toRadians(-150.0)).setJointVelocityRel(0.1));
		
		if (FingerTip.getActReq() != gripper_mode)
		{
			FingerTip.setActReq(gripper_mode);
		}

		FingerTip.setSpeed(255);
		FingerTip.setForce(5);
		
		FingerTip.setPosReq(255); // close the gripper

		ThreadUtil.milliSleep(2000); 

	} // moveToInitialPositionPositiveY
	
	private void moveToInitialPositionNegativeY()
	{
		lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-30.0), Math.toRadians(90.0), Math.toRadians(0.0), Math.toRadians(-60.0) , Math.toRadians(60.0), Math.toRadians(105.0), Math.toRadians(-100.0)).setJointVelocityRel(0.1));

		if (FingerTip.getActReq() != gripper_mode)
		{
			FingerTip.setActReq(gripper_mode);
		}

		FingerTip.setSpeed(255);
		FingerTip.setForce(5);
		
		FingerTip.setPosReq(255); // close the gripper

		ThreadUtil.milliSleep(2000); 

	} // moveToInitialPositionNegativeY
	
	// moveToInitialPosition_camera_catch_1
	private void moveToInitialPosition_camera_catch_1()
		{	
		//lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(70.13), Math.toRadians(20.34), Math.toRadians(0.06), Math.toRadians(-70.72) , Math.toRadians(-80.82), Math.toRadians(-20.79), Math.toRadians(-61.09)).setJointVelocityRel(0.3));
		lbr_iiwa_14_R820_1.move(ptp( Math.toRadians(-20.13), Math.toRadians(31.34), Math.toRadians(0.06), Math.toRadians(-94.72) , Math.toRadians(-93.82), Math.toRadians(-57.79), Math.toRadians(-61.09)).setJointVelocityRel(0.3));
		
			if (FingerTip.getActReq() != gripper_mode)
			{
				FingerTip.setActReq(gripper_mode);
			}
			FingerTip.setSpeed(255);
			FingerTip.setForce(5);
			FingerTip.setPosReq(255); // close the gripper
			ThreadUtil.milliSleep(2000); 

		} // moveToInitialPosition_camera_catch_1
		
	@Override
	public void run() {

		try {

			ToolGripper.attachTo(lbr_iiwa_14_R820_1.getFlange());
			
			moveToInitialPosition_camera_catch_1(); 
			
			initFrame = lbr_iiwa_14_R820_1.getCurrentCartesianPosition(ToolGripper.getFrame("/BasePad"));

			SmartServo aSmartServoMotion = new SmartServo(lbr_iiwa_14_R820_1.getCurrentJointPosition());

			aSmartServoMotion.useTrace(true);

			// for Automatic mode 0.25, for T1 mode 1
			aSmartServoMotion.setJointAccelerationRel(0.3);//0.3
			aSmartServoMotion.setJointVelocityRel(0.3);//0.3
			aSmartServoMotion.setMinimumTrajectoryExecutionTime(5e-3);

			
			System.out.println("Starting RealtimeMotion in Position Mode");
			if (SmartServo.validateForImpedanceMode(ToolGripper) != true)
				getLogger().info("Validation for SmartServo Compliant control failed");

//			ToolGripper.getRootFrame().moveAsync(aSmartServoMotion.setMode(mode));
			ToolGripper.getFrame("/BasePad").moveAsync(aSmartServoMotion.setMode(mode).setJointVelocityRel(1.0));
			ISmartServoRuntime theServoRuntime = aSmartServoMotion.getRuntime();
			Frame goalFrame = new Frame(); 
			Frame currentFrame = new Frame(); 

//			ForceSensorData torData = lbr_iiwa_14_R820_1.getExternalForceTorque(ToolGripper.getRootFrame());
			ForceSensorData torData = lbr_iiwa_14_R820_1.getExternalForceTorque(ToolGripper.getFrame("/BasePad/BasePadPinch_FF"));
			// Original
			// ForceSensorData torData = lbr_iiwa_14_R820_1.getExternalForceTorque(ToolGripper.getFrame("/BasePad"));

			double ForceX;
			double ForceY;
			double ForceZ;
			
			double HapticForceX;
			double HapticForceY;
			double HapticForceZ;
			
			double TorqueX;
			double TorqueY; 
			double TorqueZ; 
			
			int gripper_value=255;

			client = new YW_UDPThread(); 
			client.start(); // start the thread "UDPTestThread.java" 

			System.out.println("Client has 15 seconds to start sending data" );

			while (!client.hasReceived)		// wait for data to be received before proceeding with the rest of the code
				ThreadUtil.milliSleep(500);

			System.out.println("Go into the while" );

			while(!done)
			{		
				long startTime = System.nanoTime();
				
				theServoRuntime.updateWithRealtimeSystem();

				String[] jointStr = client.getString(); // get data from client 

				double[] jointDouble=new double[jointStr.length]; 
				
				// DEBUG
				// System.out.println("jointStr.length = " + jointStr.length);  // => jointStr.length = 15
				
				
				for(int j=0;j<jointStr.length;j++)
				{
					jointDouble[j]=Double.valueOf(jointStr[j]);
					//System.out.print("receive float data: "+jointDouble[j] + ", ");
				}
				
				
				//System.out.println();
				//System.out.println("previous mode: "+ previousMode.ordinal());
				
				// DEBUG: Print message from haptic device
				// System.out.println("Haptic = " + Arrays.toString(jointDouble));
				
				
				//FingerTip.setPosReq((int)(255-jointDouble[12]*496)); 	// max value of jointDouble[12]*496 is 255
				//FingerTip.setPosReq((int)(gripper_value)); 	// max value of jointDouble[12]*496 is 255
				
	
				goalFrame = lbr_iiwa_14_R820_1.getCurrentCartesianPosition(ToolGripper.getFrame("/BasePad"));
				aSmartServoMotion.setJointVelocityRel(0.1);
						//previousMode = p_mode.free;
						//Old_RB1_x=jointDouble[0];
						//Old_RB1_y=jointDouble[1];
						//Old_RB1_z=jointDouble[2];
							
							// KUKA goalFrame - Haptic Discrepancy FIX
							// Old_RB1_oa=jointDouble[5];
							// Old_RB1_ob=jointDouble[4];
							// Old_RB1_og=jointDouble[3];
							// Original
							//Old_RB1_oa=jointDouble[3];
							//Old_RB1_ob=jointDouble[4];
							//Old_RB1_og=jointDouble[5];

				Org_X = goalFrame.getX(); 
				Org_Y = goalFrame.getY(); 
				Org_Z = goalFrame.getZ(); 
				Org_a = goalFrame.getAlphaRad(); 
				Org_b = goalFrame.getBetaRad(); 
				Org_g = goalFrame.getGammaRad();  
						
						
						// NOTE: area of interest
						// System.out.println("Org_X=" +  Org_X);
						// System.out.println("Old_RB1_x=" +  Old_RB1_x);
				//System.out.println("ox="+Org_X+";oy="+Org_Y+";oz="+Org_Z+";oa="+Org_a+";ob="+Org_b+";og="+Org_g);
						
						
						// My Original
						// goalFrame.setX(Org_X+(jointDouble[0]*1.8-Old_RB1_x)*1000*1); // scaling by factor 1 
						// goalFrame.setY(Org_Y+(jointDouble[1]*1.8-Old_RB1_y)*1000*1); // scaling by factor 1
						// goalFrame.setZ(Org_Z+(jointDouble[2]*1.8-Old_RB1_z)*1000*1); // scaling by factor 1
						
						// KUKA goalFrame - Haptic Discrepancy FIX
						// goalFrame.setAlphaRad(Org_a+(jointDouble[5]-Old_RB1_oa)*0.8);
						// goalFrame.setBetaRad(Org_b+(jointDouble[4]-Old_RB1_ob)*0.3);
						// goalFrame.setGammaRad(Org_g+(jointDouble[3]-Old_RB1_og)*0.8);
						// Original
						//goalFrame.setX(Org_X+(jointDouble[0]*1.6-Old_RB1_x)*1000*1); // scaling by factor 1 
						//goalFrame.setY(Org_Y+(jointDouble[1]*1.6-Old_RB1_y)*1000*1); // scaling by factor 1
						//goalFrame.setZ(Org_Z+(jointDouble[2]*1.6-Old_RB1_z)*1000*1); // scaling by factor 1
						//goalFrame.setAlphaRad(Org_a+(jointDouble[3]-Old_RB1_oa)*0);
						//goalFrame.setBetaRad(Org_b+(jointDouble[4]-Old_RB1_ob)*0);
						//goalFrame.setGammaRad(Org_g+(jointDouble[5]-Old_RB1_og)*0);
						/*
				goalFrame.setX(Org_X); // scaling by factor 1 
				goalFrame.setY(Org_Y); // scaling by factor 1
				goalFrame.setZ(Org_Z); // scaling by factor 1
				goalFrame.setAlphaRad(Org_a);
				goalFrame.setBetaRad(Org_b);
				goalFrame.setGammaRad(Org_g);
				*/
				//jointDouble
				//goalFrame.setX(706.57-30); // scaling by factor 1 
				goalFrame.setX(jointDouble[0]); // scaling by factor 1 
				goalFrame.setY(jointDouble[1]); // scaling by factor 1
				goalFrame.setZ(jointDouble[2]); // scaling by factor 1
				goalFrame.setAlphaRad(jointDouble[3]);
				goalFrame.setBetaRad(jointDouble[4]);
				goalFrame.setGammaRad(jointDouble[5]);
				FingerTip.setPosReq((int)(jointDouble[6])); 	// max value of jointDouble[12]*496 is 255
				
				try{
					theServoRuntime.setDestination(goalFrame, World.Current.getRootFrame());
				}
				catch (Exception err) {
					//err.printStackTrace();
					System.out.println("setpoint out of range");
				}
				
					fingerTipForce = FingerTip.getForce(); // force will be set force, which is 5 

					torData = lbr_iiwa_14_R820_1.getExternalForceTorque(ToolGripper.getFrame("/BasePad/BasePadPinch_FF"));
					// Original
					// torData = lbr_iiwa_14_R820_1.getExternalForceTorque(ToolGripper.getFrame("/BasePad"));
					
					ForceX = torData.getForce().getX();
					ForceY = torData.getForce().getY();
					ForceZ = torData.getForce().getZ();
					
					// My Original
					HapticForceX = -1.0*ForceZ;
					HapticForceY = -1.0*ForceY;
					HapticForceZ = 1.0*ForceX;
					currentFrame = lbr_iiwa_14_R820_1.getCurrentCartesianPosition(ToolGripper.getFrame("/BasePad"));
					
					/*
					RB1_x = currentFrame.getX();
					RB1_y = currentFrame.getY();
					RB1_z = currentFrame.getZ();
					RB1_oa = currentFrame.getAlphaRad();
					RB1_ob = currentFrame.getBetaRad();
					RB1_og = currentFrame.getGammaRad();
					*/
					
					RB1_x = currentFrame.getX();
					RB1_y = currentFrame.getY();
					RB1_z = currentFrame.getZ();
					RB1_oa = currentFrame.getAlphaRad();
					RB1_ob = currentFrame.getBetaRad();
					RB1_og = currentFrame.getGammaRad();
					gripper_value=FingerTip.getFingerPos();
					
					
					//System.out.println("F_x=" +  ForceX + " F_y=" + ForceY + " F_z=" + ForceZ);
					
					// KUKA goalFrame - Haptic Discrepancy FIX
					// RB1_og = goalFrame.getAlphaRad();
					// RB1_ob = goalFrame.getBetaRad();
					// RB1_oa = goalFrame.getGammaRad();
					// Original

					
					TorqueX = torData.getTorque().getX();
					TorqueY = torData.getTorque().getY();
					TorqueZ = torData.getTorque().getZ();

					robotPosition=0; 
					jointAngle = lbr_iiwa_14_R820_1.getCurrentJointPosition().get();

					
					
					String sendStr = new String(); 
					sendStr=String.valueOf(RB1_x)+" "+String.valueOf(RB1_y)+" "+String.valueOf(RB1_z)+" "
							+String.valueOf(RB1_oa)+" "+String.valueOf(RB1_ob)+" "+String.valueOf(RB1_og) +" " 
							+String.valueOf(gripper_value)+" "
							+ String.valueOf(HapticForceX)+" "+String.valueOf(HapticForceY)+" "+String.valueOf(HapticForceZ)+" "
							+ String.valueOf(TorqueX)+" "+ String.valueOf(TorqueY)+" "+ String.valueOf(TorqueZ)+" "
							//+sendStr.valueOf(CurrentPosition.get(0))+" "+sendStr.valueOf(CurrentPosition.get(1))+" "
	                		//+sendStr.valueOf(CurrentPosition.get(2))+" "+sendStr.valueOf(CurrentPosition.get(3))+" "
	                		//+sendStr.valueOf(CurrentPosition.get(4))+" "+sendStr.valueOf(CurrentPosition.get(5))+" "
	                		//+sendStr.valueOf(CurrentPosition.get(6))+" "
							
							+ String.valueOf(fingerTipForce) + " " + String.valueOf(robotPosition) + " "
							+ String.valueOf(jointAngle[0]) + " " + String.valueOf(jointAngle[1]) + " "
							+ String.valueOf(jointAngle[2]) + " " + String.valueOf(jointAngle[3]) + " "
							+ String.valueOf(jointAngle[4]) + " " + String.valueOf(jointAngle[5]) + " "
							+ String.valueOf(jointAngle[6]) + '\0';
					// System.out.printf("sendStr=%s\n" ,sendStr);

					//try{
						if (client.sendMsg(sendStr))
						{
							//System.out.println("Message sending succeeded"); 
						}
						else
						{
							System.out.println("Message sending failed"); 
						}
					//}
					//catch (Exception err) {
					//	err.printStackTrace();
					//}

				
				
				// TIMER
				long endTime = System.nanoTime();
				
				long duration = (endTime - startTime);
				// System.out.println(duration/1000000 + " miliseconds");
				
			} // while
		}// try 

		catch (IOException e1) {
			e1.printStackTrace();
		}
	} // run 

	public static void main(String[] args) {
		YW_UDP_Server app = new YW_UDP_Server();
		app.runApplication();
	}

} // class
