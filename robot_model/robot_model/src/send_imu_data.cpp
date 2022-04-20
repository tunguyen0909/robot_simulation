#include "ros/ros.h"
// #include "geometry_msgs/Twist.h"
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <std_msgs/Header.h>
#include <sensor_msgs/Imu.h>
#include <math.h>

#include <stdio.h>
#include "ceSerial.h"
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
using namespace std;
using namespace ce;

class Imu_cals{
public:
    Imu_cals();
    void spin();
    // void velCallback(const geometry_msgs::Twist& vel);
private:
    ros::NodeHandle n;
   
    ros::Publisher imu_pub;

    tf::TransformBroadcaster odom_broadcaster;

    ceSerial com; // Linux

    double linear_vel_x_;
    double linear_vel_y_;
    double angular_vel_z_;
    ros::Time last_vel_time_;
    double vel_dt_;
    double x_pos_;
    double y_pos_;
    double heading_;

    double q_x, q_y, q_z, q_w;
    double rate;
    int a;
    char RX[25];
    float num[4];
    int i = 0;
    int j = 0;


    void init_variables();
    void update();
    

    void Serial_init();
    

};



Imu_cals::Imu_cals(): com("/dev/ttyUSB1",115200,8,'N',1){
    Serial_init();
    init_variables();

    imu_pub = n.advertise<sensor_msgs::Imu>("/imu/data", 50);
    // velocity_sub_ = n.subscribe("raw_vel", 50, &Odommetry_cals::velCallback, this);
    // velocity_sub_ = n.subscribe("raw_vel", 50, &Odommetry_cals::velCallback, this);

}

void Imu_cals::init_variables(){
    linear_vel_x_ = 0;
    linear_vel_y_ = 0;
    angular_vel_z_ = 0;
    last_vel_time_ = ros::Time::now();
    vel_dt_ = 0;
    x_pos_ = 0;
    y_pos_ = 0;
    heading_ = 0;

    q_x = 0;
    q_y = 0;
    q_z = 0;
    q_w = 0;

    rate = 10;

    // std::memset(RX, 0, sizeof(RX));
}


void Imu_cals::update(){
    bool successFlag;
    // std::memset(RX, 0, sizeof(RX));
    char c=com.ReadChar(successFlag); // read a char
    // printf("%c\n",c);
    if(successFlag)
    { 
        //A:65 B:66 " ": 32
        if(c != 'A')
        {
            if(c != 'B')
            {
                if(c >= 46 && c <= 57 || c == 32 || c == 45)
                {
                    RX[i] = c;
                    i++;
                }
            }
        }
        
        if(c == 'B')
        {
            i = 0;
            //float num = atof(dataTX);
            //printf("%0.2f\r\n",num);
            //printf("%s\r\n",dataTX);
            char *ptr;
            ptr = strtok(RX," ");
            while(ptr != NULL)
            {
                num[j] = atof(ptr);
                printf("%0.2f\n",num[j]);
                ptr = strtok(NULL," ");
                j++;
                if(j == 4)
                {
                    j = 0;
                    break;
                }
            }
            //memset(dataTX,'0',25);
        }
    }

    q_x = num[0];
    q_y = num[1];
    q_z = num[2];
    q_w = num[3];

    // printf("%lf %lf %lf %lf\n", q_x, q_y, q_z, q_w);

    sensor_msgs::Imu imu_msgs;

    std_msgs::Header h;
    h.stamp = ros::Time::now();
    h.frame_id = "imu_link";

    imu_msgs.header = h;

    imu_msgs.orientation.x = q_x;
    imu_msgs.orientation.y = q_y;
    imu_msgs.orientation.z = q_z;
    imu_msgs.orientation.w = q_w;
    imu_msgs.orientation_covariance = {-1, -1, -1, -1, -1, -1, -1, -1, -1};	
    imu_msgs.angular_velocity_covariance = {-1, -1, -1, -1, -1, -1, -1, -1, -1};
    imu_msgs.linear_acceleration_covariance = {-1, -1, -1, -1, -1, -1, -1, -1, -1};
    // ROS_INFO("%c", RX[i]);

    imu_pub.publish(imu_msgs);

}

void Imu_cals::spin(){
    // ros::Rate loop_rate(rate);

    while (ros::ok()){
        update();
        // loop_rate.sleep();
    }
}

void Imu_cals::Serial_init(){
    
    printf("Opening port %s.\n",com.GetPort().c_str());
    printf("%li", com.Open());
	if (com.Open() == 0) {
		printf("OK.\n");
	}
	else {
		printf("Error.\n");
	}
}

void my_handler(int s){
           printf("Caught signal %d\n",s);
           exit(1); 

}



int main(int argc, char** argv){
    ros::init(argc, argv,"send_imu");
    signal (SIGINT,my_handler);
    Imu_cals obj;
    // ros::spin();
    obj.spin();
    return 0;
}

