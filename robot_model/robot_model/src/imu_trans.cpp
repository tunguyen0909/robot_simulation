#include "ros/ros.h"
// #include "geometry_msgs/Twist.h"
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <sensor_msgs/Imu.h>
#include <math.h>

class Odommetry_cals{
public:
    Odommetry_cals();
    void velCallback(const sensor_msgs::Imu& imu_data);
private:
    ros::NodeHandle n;
    ros::Subscriber velocity_sub_;
    ros::Publisher odom_pub;

    tf::TransformBroadcaster odom_broadcaster;

    double linear_vel_x_;
    double linear_vel_y_;
    double angular_vel_z_;
    ros::Time last_vel_time_;
    double vel_dt_;
    double x_pos_;
    double y_pos_;
    double heading_;

    void init_variables();
    

};



Odommetry_cals::Odommetry_cals(){
    init_variables();

    odom_pub = n.advertise<nav_msgs::Odometry>("raw_odom", 50);
    velocity_sub_ = n.subscribe("imu/data", 50, &Odommetry_cals::velCallback, this);
    // velocity_sub_ = n.subscribe("raw_vel", 50, &Odommetry_cals::velCallback, this);

}

void Odommetry_cals::init_variables(){
    linear_vel_x_ = 0;
    linear_vel_y_ = 0;
    angular_vel_z_ = 0;
    last_vel_time_ = ros::Time::now();
    vel_dt_ = 0;
    x_pos_ = 0;
    y_pos_ = 0;
    heading_ = 0;
}

void Odommetry_cals::velCallback(const sensor_msgs::Imu& imu_data){
    ros::Time now = ros::Time::now();

    // linear_vel_x_ = vel.linear.x;
    // linear_vel_y_ = vel.linear.y;
    // angular_vel_z_ = vel.angular.z;

    // vel_dt_ = (now - last_vel_time_).toSec();
    // last_vel_time_ = now;

    // double delta_heading = angular_vel_z_ * vel_dt_; //radians
    // double delta_x = (linear_vel_x_ * cos(heading_) - linear_vel_y_ * sin(heading_)) * vel_dt_; //m
    // double delta_y = (linear_vel_x_ * sin(heading_) + linear_vel_y_ * cos(heading_)) * vel_dt_; //m

    // x_pos_ += delta_x;
    // y_pos_ += delta_y;
    // heading_ += delta_heading;

    // ROS_INFO("GOc quay la: %lf", heading_ * 180 / 3.14159);

    // geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(heading_);

    geometry_msgs::TransformStamped odom_trans;
    odom_trans.header.stamp = now;
    odom_trans.header.frame_id = "odom";
    odom_trans.child_frame_id = "imu_link";


    odom_trans.transform.translation.x = 0.0;
    odom_trans.transform.translation.y = 0.0;
    odom_trans.transform.translation.z = 0.0;
    odom_trans.transform.rotation.x = imu_data.orientation.x;
    odom_trans.transform.rotation.y = imu_data.orientation.y;
    odom_trans.transform.rotation.z = imu_data.orientation.z;
    odom_trans.transform.rotation.w = imu_data.orientation.w;

    odom_broadcaster.sendTransform(odom_trans);


    nav_msgs::Odometry odom;
    odom.header.stamp = now;
    odom.header.frame_id = "odom";


    odom.pose.pose.position.x = 0.0;
    odom.pose.pose.position.y = 0.0;
    odom.pose.pose.position.z = 0.0;
    odom.pose.pose.orientation = imu_data.orientation;

    odom.child_frame_id = "base_footprint";
    odom.twist.twist.linear.x = 0.0;
    odom.twist.twist.linear.y = 0.0;
    odom.twist.twist.angular.z = 0.0;

    odom_pub.publish(odom);
}

int main(int argc, char** argv){
    ros::init(argc, argv,"imu_trans");
    Odommetry_cals obj;
    ros::spin();
    return 0;
}

