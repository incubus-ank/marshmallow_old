/*
*  3iRoboticsLIDAR System II
*  Driver Interface
*
*  Copyright 2017 3iRobotics
*  All rights reserved.
*
*	Author: 3iRobotics, Data:2017-09-15
*
*/

#ifdef _MSC_VER
#ifndef _USE_MATH_DEFINES
#define _USE_MATH_DEFINES
#endif
#endif

#include <math.h>
#include <unistd.h>

#include <chrono>
#include <iostream>
#include <memory>

#include "rclcpp/clock.hpp"
#include "rclcpp/rclcpp.hpp"
#include "rclcpp/time_source.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include <vector>
#include <iostream>
#include <string>
#include <signal.h>

#define DEG2RAD(x) ((x)*M_PI/180.)

#include "C3iroboticsLidar.h"
#include "../sdk/include/CSerialConnection.h"


typedef struct _rslidar_data
{
    _rslidar_data()
    {
        signal = 0;
        angle = 0.0;
        distance = 0.0;
    }
    uint8_t signal;
    float   angle;
    float   distance;
}RslidarDataComplete;


using namespace std;
using namespace everest::hwdrivers;

// void publish_scan(rclcpp::Publisher *pub,
//                   _rslidar_data *nodes,
//                   size_t node_count, ros::Clock start,
//                   double scan_time,
//                   float angle_min, float angle_max,
//                   std::string frame_id)
// {
//     auto scan_msg = std::make_shared<sensor_msgs::msg::LaserScan>();

//     scan_msg->header.stamp = start;
//     scan_msg->header.frame_id = frame_id;
//     scan_msg->angle_min = angle_min;
//     scan_msg->angle_max = angle_max;
//     scan_msg->angle_increment = (scan_msg->angle_max - scan_msg->angle_min) / (360.0f - 1.0f);

//     scan_msg->scan_time = scan_time;
//     scan_msg->time_increment = scan_time / (double)(node_count-1);
//     scan_msg->range_min = 0.15;
//     scan_msg->range_max = 5.0;

//     scan_msg->ranges.resize(360, std::numeric_limits<float>::infinity());
//     scan_msg->intensities.resize(360, 0.0);

//     //Unpack data
//     for (size_t i = 0; i < node_count; i++)
//     {
//         size_t current_angle = floor(nodes[i].angle);
//         if(current_angle > 360.0)
//         {
//             printf("Lidar angle is out of range %d\n", (int)current_angle);
//             continue;
//         }
//         float read_value = (float) nodes[i].distance;
//         if (read_value < scan_msg.range_min || read_value > scan_msg.range_max)
//             scan_msg.ranges[360- 1- current_angle] = std::numeric_limits<float>::infinity();
//         else
//             scan_msg.ranges[360 -1- current_angle] = read_value;

// 		float intensities = (float) nodes[i].signal;
// 		scan_msg.intensities[360 -1- current_angle] = intensities;

// 	}

//     pub->publish(*scan_msg);
// }

int main(int argc, char * argv[])
{
    // read ros param
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("delta_2b_lidar_node");

	int    opt_com_baudrate = 230400;
	string opt_com_path = "/dev/ttyUSB0";
    string frame_id = "laser";
    string lidar_scan;

    // ros::NodeHandle nh;
    // ros::NodeHandle nh_private("~");
    // nh_private.param<string>("serial_port", opt_com_path, "/dev/ttyUSB4");
    // nh_private.param<string>("frame_id", frame_id, "laser");

    auto scan_pub = node->create_publisher<sensor_msgs::msg::LaserScan>("scan", 1000);
    rclcpp::WallRate loop_rate(20);

    CSerialConnection serial_connect;
    C3iroboticsLidar robotics_lidar;

    serial_connect.setBaud(opt_com_baudrate);
    serial_connect.setPort(opt_com_path.c_str());
    if(serial_connect.openSimple())
    {
        printf("[AuxCtrl] Open serail port sucessful!\n");
    }
    else
    {
        printf("[AuxCtrl] Open serail port %s failed! \n", opt_com_path.c_str());
        return -1;
    }

    printf("3iRoboticsLidar connected\n");

    robotics_lidar.initilize(&serial_connect);

    rclcpp::Clock system_clock;

    rclcpp::Time start_scan_time = system_clock.now();
    rclcpp::Time end_scan_time;
    double scan_duration;

    while (rclcpp::ok())
    {
		TLidarGrabResult result = robotics_lidar.getScanData();
        switch(result)
        {
            case LIDAR_GRAB_ING:
            {
                break;
            }
            case LIDAR_GRAB_SUCESS:
            {
                TLidarScan lidar_scan = robotics_lidar.getLidarScan();
                size_t lidar_scan_size = lidar_scan.getSize();
                std::vector<RslidarDataComplete> send_lidar_scan_data;
                send_lidar_scan_data.resize(lidar_scan_size);
                RslidarDataComplete one_lidar_data;
                for(size_t i = 0; i < lidar_scan_size; i++)
                {
                    one_lidar_data.signal = lidar_scan.signal[i];
                    one_lidar_data.angle = lidar_scan.angle[i];
                    one_lidar_data.distance = lidar_scan.distance[i];
                    send_lidar_scan_data[i] = one_lidar_data;
                }

            	float angle_min = DEG2RAD(0.0f);
            	float angle_max = DEG2RAD(359.0f);

				end_scan_time = system_clock.now();
				scan_duration = (end_scan_time - start_scan_time).seconds() * 1e-3;
                printf("Receive Lidar count %u!\n", lidar_scan_size);

                //if successful, publish lidar scan
                int start_node = 0, end_node = 359;
                // publish_scan(&scan_pub, &send_lidar_scan_data[0], lidar_scan_size,
                //          start_scan_time, scan_duration,
                //          angle_min, angle_max,
                //          frame_id);
                // void publish_scan(rclcpp::Publisher *pub,
            //                   _rslidar_data *nodes,
            //                   size_t node_count, ros::Clock start,
            //                   double scan_time,
            //                   float angle_min, float angle_max,
            //                   std::string frame_id)

                _rslidar_data *nodes = &send_lidar_scan_data[0];
                size_t node_count = lidar_scan_size;
                rclcpp::Time start = start_scan_time;
                double scan_time = scan_duration;

                auto scan_msg = std::make_shared<sensor_msgs::msg::LaserScan>();

                scan_msg->header.stamp = start;
                scan_msg->header.frame_id = frame_id;
                scan_msg->angle_min = angle_min;
                scan_msg->angle_max = angle_max;
                scan_msg->angle_increment = (scan_msg->angle_max - scan_msg->angle_min) / (360.0f - 1.0f);

                scan_msg->scan_time = scan_time;
                scan_msg->time_increment = scan_time / (double)(node_count-1);
                scan_msg->range_min = 0.15;
                scan_msg->range_max = 5.0;

                scan_msg->ranges.resize(360, std::numeric_limits<float>::infinity());
                scan_msg->intensities.resize(360, 0.0);

                //Unpack data
                for (size_t i = 0; i < node_count; i++)
                {
                    size_t current_angle = floor(nodes[i].angle);
                    if(current_angle > 360.0)
                    {
                        printf("Lidar angle is out of range %d\n", (int)current_angle);
                        continue;
                    }
                    float read_value = (float) nodes[i].distance;
                    if (read_value < scan_msg->range_min || read_value > scan_msg->range_max)
                        scan_msg->ranges[360- 1- current_angle] = std::numeric_limits<float>::infinity();
                    else
                        scan_msg->ranges[360 -1- current_angle] = read_value;

                    float intensities = (float) nodes[i].signal;
                    scan_msg->intensities[360 -1- current_angle] = intensities;

                }

                scan_pub->publish(*scan_msg);
            
				start_scan_time = end_scan_time;

                break;
            }
            case LIDAR_GRAB_ERRO:
            {
                break;
            }
            case LIDAR_GRAB_ELSE:
            {
                printf("[Main] LIDAR_GRAB_ELSE!\n");
                break;
            }
        }
        usleep(50);
        rclcpp::spin_some(node);
    }

    return 0;
}
