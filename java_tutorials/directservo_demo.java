package com.kuka.roboticsAPI.directServo.samples;

import static com.kuka.roboticsAPI.motionModel.BasicMotions.ptp;

import com.kuka.common.StatisticTimer;
import com.kuka.common.StatisticTimer.OneTimeStep;
import com.kuka.common.ThreadUtil;
import com.kuka.roboticsAPI.applicationModel.RoboticsAPIApplication;
import com.kuka.roboticsAPI.deviceModel.JointPosition;
import com.kuka.roboticsAPI.deviceModel.LBR;
import com.kuka.roboticsAPI.deviceModel.OperationMode;
import com.kuka.roboticsAPI.geometricModel.PhysicalObject;
import com.kuka.roboticsAPI.motionModel.DirectServo;
import com.kuka.roboticsAPI.motionModel.IDirectServoRuntime;
import com.kuka.roboticsAPI.userInterface.ServoMotionUtilities;

/**
 * Very simple sample of JointSpecific DirectServo Motion
 *
 * What you should learn in this lesson:
 *
 * <ul>
 * <li>Activation of a DirectServo motion in default control mode
 * <li>Sending a sequence joint specific setpoints
 * <li>the Action of the StatisticTimer for evaluating bandwith/Timing Issues
 * </ul>
 *
 * @author schreiberg
 *
 */
public class DirectServoSampleSimpleJointMotion extends RoboticsAPIApplication
{
    // members
    private LBR _theLbr;
    /**
     * Will be initialized from the routine "createTool()"
     *
     * IMPORTANT NOTE: Set the load mass properly
     */
    private PhysicalObject _toolAttachedToLBR;
    private IDirectServoRuntime theDirectServoRuntime = null;

    @Override
    public void initialize()
    {

        // Locate the "first" Lightweight Robot in the system
        _theLbr = ServoMotionUtilities.locateLBR(getContext());
        // FIXME: Set proper Weights or use the plugin feature
        double translationOfTool[] =
        { 0, 0, 100 };
        double mass = 0;
        double centerOfMassInMillimeter[] =
        { 0, 0, 100 };
        _toolAttachedToLBR = ServoMotionUtilities.createTool(_theLbr,
                "SimpleJointMotionSampleTool", translationOfTool, mass,
                centerOfMassInMillimeter);

    }

    /**
     * Move to an initial Position WARNING: MAKE SHURE, THAT the pose is
     * collision free
     */
    public void moveToInitialPosition()
    {
        _toolAttachedToLBR.move(
                ptp(0., Math.PI / 180 * 30., 0., -Math.PI / 180 * 60., 0.,
                        Math.PI / 180 * 90., 0.).setJointVelocityRel(0.1));
        /*
         *
         * For Completeness Sake, the validation is performed here Even it would
         * not be necessary within this sample.
         *
         * As long, as you'd remain within position control, the validation is
         * not neccessary ... but, lightweight robot without ImpedanceControl is
         * a car without fuel...
         *
         * Note: The Validation itself justifies, that in this very time
         * instance, the load parameter setting was sufficient. This does not
         * mean by far, that the parameter setting is valid in the sequel or
         * lifetime of this program
         */
        try
        {
            if (DirectServo.validateForImpedanceMode(_toolAttachedToLBR) != true)
            {
                System.out
                        .println("Validation of Torque Model failed - correct your mass property settings");
                System.out
                        .println("DirectServo will be available for position controlled mode only, until validation is performed");
            }
        }
        catch (IllegalStateException e)
        {
            System.out.println("Omitting validation failure for this sample\n"
                    + e.getMessage());
        }
    }

    // Sleep in between
    int _milliSleepToEmulateComputationalEffort = 0;
    private int _numRuns = 10000;
    private double _amplitude = 0.3;
    private double _freqency = 0.1;
    private static int steps = 0;

    public void run()
    {

        moveToInitialPosition();

        JointPosition initialPosition = new JointPosition(
                _theLbr.getCurrentJointPosition());
        DirectServo aDirectServoMotion = new DirectServo(initialPosition);

        aDirectServoMotion.setMinimumTrajectoryExecutionTime(8e-3);

        System.out.println("Starting DirectServoMotion in Position Mode");
        _toolAttachedToLBR.getDefaultMotionFrame().moveAsync(aDirectServoMotion);

        // Fetch the Runtime of the Motion part
        // NOTE: the Runtime exists AFTER motion command was issued
        theDirectServoRuntime = aDirectServoMotion
                .getRuntime();

        // create an JointPosition Instance, to play with
        JointPosition destination = new JointPosition(
                _theLbr.getJointCount());
        System.out.println("start loop");
        // For Roundtrip time measurement...
        StatisticTimer timing = new StatisticTimer();
        try
        {
            if (_theLbr.getOperationMode() == OperationMode.T1)
            {
                // React on T1 Mode - use less amplitude ...
                _amplitude = 0.2;
            }

            // do a cyclic loop
            // Refer to some timing...
            // in nanosec
            double omega = _freqency * 2 * Math.PI * 1e-9;
            long startTimeStamp = System.nanoTime();
            for (steps = 0; steps < _numRuns; ++steps)
            {
                // Timing - draw one step
                OneTimeStep aStep = timing.newTimeStep();
                // ///////////////////////////////////////////////////////
                // Insert your code here
                // e.g Visual Servoing or the like
                // emulate some computational effort - or waiting for external
                // stuff
                ThreadUtil.milliSleep(_milliSleepToEmulateComputationalEffort);
                theDirectServoRuntime.updateWithRealtimeSystem();
                // Get the measured position
                JointPosition curMsrJntPose = theDirectServoRuntime
                        .getAxisQMsrOnController();

                double curTime = System.nanoTime() - startTimeStamp;
                double sinArgument = omega * curTime;

                for (int k = 0; k < destination.getAxisCount(); ++k)
                {
                    destination.set(k, Math.sin(sinArgument)
                            * _amplitude + initialPosition.get(k));
                    if (k > 5)
                    {
                        destination.set(k, initialPosition.get(k));
                    }
                }
                theDirectServoRuntime
                        .setDestination(destination);
                // Overall timing end
                aStep.end();

            } // end for
        }
        catch (Exception e)
        {
            System.out.println(e);
            e.printStackTrace();
        }
        ThreadUtil.milliSleep(1000);
        // /////////////////////////////////////////////////
        // Do or die: print statistics and parameters of the motion
        System.out.println("Displaying final states after loop ");
        System.out.println(getClass().getName() + " \n" + theDirectServoRuntime.toString());
        // Stop the motion
        theDirectServoRuntime.stopMotion();
        System.err.println("Statistic Timing of Overall Loop " + timing);
        if (timing.getMeanTimeMillis() > 80)
        {
            System.out
                    .println("Statistic Timing is unexpected slow, you should try to optimize TCP/IP Transfer");
            System.out
                    .println("The TCP/IP Stack is too slow - see the manual for details");
        }
    }

    /**
     * Main routine, which starts the application
     */
    public static void main(String[] args)
    {
        DirectServoSampleSimpleJointMotion app = new DirectServoSampleSimpleJointMotion();
        app.runApplication();

    }
}