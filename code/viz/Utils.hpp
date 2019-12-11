#ifndef UTILS_H
#define UTILS_H

#include <set>
#include <map>
#include <cmath>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>

#include <glm/vec3.hpp>
#include <boost/algorithm/string.hpp>

//https://github.com/fmi-alg/libdts2
//https://rspatial.org/sphere/sphere.pdf
//http://www.songho.ca/opengl/gl_sphere.html
//http://www.movable-type.co.uk/scripts/latlong.html
//https://stackoverflow.com/questions/545870/algorithm-to-compute-a-voronoi-diagram-on-a-sphere

//https://mathematica.stackexchange.com/questions/78705/plot-a-partition-of-the-sphere-given-vertices-of-polygons

//http://www.geuz.org/gl2ps/

//https://mathematica.stackexchange.com/questions/139457/voronoi-grid-on-a-sphere

struct Mouse
{
    int x, y, button, state;
};

struct Vec3d
{
    double x, y, z;
};

struct LonLat
{
    double lon, lat;
};

Vec3d Spherical2Cartesian(const LonLat& lola, const double& R = 1)
{
    double x = R * std::cos(lola.lat) * std::cos(lola.lon);
    double y = R * std::cos(lola.lat) * std::sin(lola.lon);
    double z = R * std::sin(lola.lat);
    return Vec3d{ x, y, z };
}

LonLat Cartesian2Spherical(const Vec3d& vec3d, const double& R = 1)
{
    double lat = std::asin(vec3d.z / R);
    double lon = std::atan2(vec3d.y, vec3d.x);
    LonLat res;
    res.lat = lat;
    res.lon = lon;
    return res;
}

Vec3d split_arc(const Vec3d& pp1, const Vec3d& pp2)
{
    auto p1 = Cartesian2Spherical(pp1);
    auto p2 = Cartesian2Spherical(pp2);

    auto& f1 = p1.lat;
    auto& f2 = p2.lat;
    auto& l1 = p1.lon;
    auto& l2 = p2.lon;

    auto Bx = std::cos(f2) * std::cos(l2 - l1);
    auto By = std::cos(f2) * std::sin(l2 - l1);
    auto f3 = std::atan2(std::sin(f1) + std::sin(f2),
        std::sqrt((std::cos(f1) + Bx) * (std::cos(f1) + Bx) + By * By));
    auto l3 = l1 + std::atan2(By, std::cos(f1) + Bx);

    LonLat res;
    res.lat = f3;
    res.lon = l3;

    return Spherical2Cartesian(res);
}

Vec3d split_arc2(const Vec3d& pp1, const Vec3d& pp2, const double frac, const double R = 1)
{
    auto p1 = Cartesian2Spherical(pp1);
    auto p2 = Cartesian2Spherical(pp2);

    auto& f1 = p1.lat;
    auto& f2 = p2.lat;
    auto& l1 = p1.lon;
    auto& l2 = p2.lon;

    auto beta = std::acos(std::sin(f1) * std::sin(f2) 
        + std::cos(f1) * std::cos(f2) * std::cos(l1 - l2));

    auto a = std::sin((1 - frac) * beta) / sin(beta);
    auto b = std::sin(frac * beta) / std::sin(beta);
    auto x = a * std::cos(f1) * std::cos(l1) + b * std::cos(f2) * std::cos(l2);
    auto y = a * std::cos(f1) * std::sin(l1) + b * std::cos(f2) * std::sin(l2);
    auto z = a * std::sin(f1) + b * std::sin(f2);
    auto fi = std::atan2(z, std::sqrt(x * x + y * y));
    auto li = std::atan2(y, x);

    LonLat res;
    res.lat = fi;
    res.lon = li;

    return Spherical2Cartesian(res);
}

std::vector<Vec3d> readXYZ(const std::string& fileName)
{
    std::vector<Vec3d> points;
    std::ifstream inFile(fileName);    

    for (std::string line; std::getline(inFile, line); )
    {
        std::vector<std::string> parts;
        boost::algorithm::split(parts, line, boost::is_any_of(" "), boost::token_compress_on);

        if (boost::algorithm::iequals("LA", parts[0]))
        {
            Vec3d point = { std::stod(parts[1]), std::stod(parts[2]), std::stod(parts[3]) };
            points.push_back(point);
        }
    }

    inFile.close();

    return points;
}

std::map<int, int> readColoring(const std::string& fileName)
{
    std::map<int, int> coloring;
    std::ifstream inFile(fileName);

    for (std::string line; std::getline(inFile, line); )
    {
        std::vector<std::string> parts;
        boost::algorithm::split(parts, line, boost::is_any_of(" "), boost::token_compress_on);

        if (boost::algorithm::iequals("l", parts[0]))
        {
            coloring[std::stoi(parts[1])] = std::stoi(parts[2]);
        }
    }

    inFile.close();

    return coloring;
}

std::vector<std::pair<int, int>> readTriangEdges(const std::string& fileName)
{
    std::vector<std::pair<int, int>> edges;
    std::ifstream inFile(fileName);

    for (std::string line; std::getline(inFile, line); )
    {
        std::vector<std::string> parts;
        boost::algorithm::split(parts, line, boost::is_any_of(" "), boost::token_compress_on);

        if (boost::algorithm::iequals("e", parts[0]))
        {            
            edges.push_back({ std::stoi(parts[1]), std::stoi(parts[2]) });
        }
    }

    inFile.close();

    return edges;
}

std::vector<std::vector<Vec3d>> readFaces(const std::string& fileName)
{
    std::vector<std::vector<Vec3d>> faces;

    std::ifstream inFile(fileName);

    std::vector<Vec3d> face;
    for (std::string line; std::getline(inFile, line); )
    {
        boost::trim(line);
        if (line.empty())
        {            
            if (!face.empty())
            {
                faces.push_back(face);
                face.clear();
            }    
            continue;
        }

        std::vector<std::string> parts;
        boost::algorithm::split(parts, line, boost::is_any_of(" "), boost::token_compress_on);
        Vec3d point = { std::stod(parts[0]), std::stod(parts[1]), std::stod(parts[2]) };
        face.push_back(point);        
    }

    if (!face.empty())
    {
        faces.push_back(face);
        face.clear();
    }

    inFile.close();
    
    return faces;
}

std::vector<Vec3d> upgrade_face(std::vector<Vec3d> face)
{
    std::vector<Vec3d> newFace;

    auto l = face.size(); 
    for (size_t i = 0; i < l; i++)
    {
        auto& p1 = face[i];
        auto& p2 = face[(i + 1) % l];

        for (double d = 0; d <= 1; d += 0.005)
        {
            newFace.push_back(split_arc2(p1, p2, d));
        }
    }

    return newFace;
}

#endif