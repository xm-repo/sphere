
#include "Utils.hpp"
#include <gl2ps-1.4.0-source/gl2ps.h>
#include <freeglut/include/GL/glut.h>
#include <glm/vec3.hpp>

Mouse mouse = {0, 0};
double cameraDistance = 3.5;
std::pair<double, double> cameraAngleXY(0, 0), cameraTransXY(0, 0);
std::pair<int, int> screenWH;

std::string fileName;
std::string nColors;
std::vector<Vec3d> points;
std::map<int, int> coloring;
std::set<std::pair<int, int>> sedges, sedges2, sedges3;
std::vector<std::pair<int, int>> edges, edges2;
std::vector<std::vector<Vec3d>> faces, faces2;
std::vector<GLfloat> facesTriangles;

std::string vshader =
"#version 330 core"
"layout(location = 0) in vec3 pos;"
"void main() {"
    "gl_Position.xyz = pos;"    
"}";

std::vector<Vec3d> palette =
{
    { 0.0, 0.0, 0.0 },
    { 1.0, 0.0, 0.0 },
    { 0.0, 1.0, 0.0 },
    { 1.0, 1.0, 0.0 },
    { 0.0, 0.0, 1.0 },
    { 0.60, 0.40, 0.12 },
    { 1.0, 0.0, 1.0 },
    { 0.75, 0.75, 0.75 },
    { 0.0, 1.0, 1.0 },
    { 0.25, 0.25, 0.25 },    
    { 0.98, 0.625, 0.12 },
    { 0.98, 0.04, 0.7 },
    { 0.60, 0.40, 0.70 },
    { 1.0, 1.0, 1.0 },
};

bool drawPoints = false;
bool drawSphere = false;
bool drawG = false;
bool drawG2 = false;
bool drawFaces = true;
bool drawColors = true;
bool drawAxes = false;
bool drawFacesSkeletons = false;


void DisplayCallback();
void DoDraw();

void save(const std::string& fileName, int type = GL2PS_PDF)
{
    FILE *fp;
    GLint buffsize = 0, state = GL2PS_OVERFLOW;
    fp = fopen(fileName.c_str(), "wb");
    printf("Saving ... \n");
    while (state == GL2PS_OVERFLOW) {
        buffsize += 1024 * 1024;
        gl2psBeginPage("test", "gl2psTestSimple", NULL,
            GL2PS_PDF, GL2PS_SIMPLE_SORT,
            GL2PS_DRAW_BACKGROUND | GL2PS_USE_CURRENT_VIEWPORT,
            GL_RGBA, 0, NULL, 100, 100, 100, buffsize, fp, fileName.c_str());
        DisplayCallback();
        state = gl2psEndPage();
    }
    fclose(fp);
    printf("Done \n");
}

void DisplayCallback()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

    /*
    glPushMatrix();
    glTranslatef(-2, -2, 0);
    DoDraw();
    glPopMatrix();

    glPushMatrix();
    glRotatef(180, 0, 1, 0);
    glTranslatef(-2, 2, 0);   
    DoDraw();
    glPopMatrix();

    glPushMatrix();
    glTranslatef(2, 2, 0);
    DoDraw();
    glPopMatrix();

    glPushMatrix();
    glTranslatef(2, -2, 0);
    DoDraw();
    glPopMatrix();
    */

    DoDraw();
    glFlush();
    glutSwapBuffers();
}

void DoDraw()
{
    glPushMatrix();

    //camera
    {
        glTranslatef(cameraTransXY.first, cameraTransXY.second, -cameraDistance);
        glRotatef(cameraAngleXY.first, 1, 0, 0);
        glRotatef(cameraAngleXY.second, 0, 1, 0);        
    }

    if (drawSphere)
    {
        glColor4f(0.3f, 0.3f, 0.3f, 1.f);
        //glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
        glutSolidSphere(0.99f, 100, 100);
    }

    if (drawPoints)
    {
        int i = 0;
        //auto p = points[15];
        for (auto& p : points)
        {
            if (drawColors)
            {
                const auto& clr = palette[coloring[i + 1]];
                glColor4f(clr.x, clr.y, clr.z, 1.f);
            }
            else
            {
                glColor4f(0.0f, 0.0f, 1.0f, 1.f);
            }

            i++;
            glPushMatrix();
            glTranslatef(p.x, p.y, p.z);
            glutSolidSphere(0.03f, 10, 10);
            glPopMatrix();
        }
    }

    if (drawG)
    {
        glColor4f(1.0f, 0.0f, 0.0f, 1.5f);

        for (auto& e : edges)
        {
            //if (e.first - 1 != 15)
            //{
            //    continue;
            //}
            auto& p1 = points[e.first - 1];
            auto& p2 = points[e.second - 1];
            glBegin(GL_LINES);
            glVertex3f(p1.x, p1.y, p1.z);
            glVertex3f(p2.x, p2.y, p2.z);
            glEnd();
        }
    }

    if (drawG2)
    {
        glColor4f(0.0f, 0.3f, 0.0f, 1.2f);

        for (auto& e : sedges3)
        {
            //if (e.first - 1 != 15)
            //{
            //    continue;
            //}
            auto& p1 = points[e.first - 1];
            auto& p2 = points[e.second - 1];
            glBegin(GL_LINES);
            glVertex3f(p1.x, p1.y, p1.z);
            glVertex3f(p2.x, p2.y, p2.z);
            glEnd();
        }
    }

    if (drawFacesSkeletons)
    {
        glPushMatrix();

        for (auto& face : faces)
        {
            glColor4f(0.6f, 0.3f, 0.2f, 1.f);
            for (size_t i = 0; i < face.size(); i++)
            {
                auto& p1 = face[i];
                auto& p2 = face[(i + 1) % face.size()];

                glBegin(GL_LINES);
                glVertex3f(p1.x, p1.y, p1.z);
                glVertex3f(p2.x, p2.y, p2.z);
                glEnd();
            }            
        }

        glPopMatrix();
    }
    
    if (drawFaces)
    {
        glPushMatrix();

        glLineWidth(2.f);

        int i = 0;
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        //auto& face = faces[15];
        for (auto& face : faces2)
        {
            auto l = face.size();

            if (drawColors)
            {
                const auto& clr = palette[coloring[i + 1]];
                glColor4f(clr.x, clr.y, clr.z, 1.f);
            }
            else
            {
                glColor4f(0.6f, 0.3f, 0.2f, 1.f);
            }

            auto& c = points[i];
            std::vector<GLfloat> triangles;
            for (size_t j = 0; j < l; j++)
            {
                auto& p1 = face[j];
                auto& p2 = face[(j + 1) % l];

                //glBegin(GL_TRIANGLES);
                //glVertex3f(p1.x, p1.y, p1.z);
                //glVertex3f(p2.x, p2.y, p2.z);
                //glVertex3f(c.x, c.y, c.z);
                //glEnd();

                triangles.push_back(p1.x);
                triangles.push_back(p1.y);
                triangles.push_back(p1.z);

                triangles.push_back(p2.x);
                triangles.push_back(p2.y);
                triangles.push_back(p2.z);

                triangles.push_back(c.x);
                triangles.push_back(c.y);
                triangles.push_back(c.z);
            }
            glEnableClientState(GL_VERTEX_ARRAY);
            glVertexPointer(3, GL_FLOAT, 0, triangles.data());
            glDrawArrays(GL_TRIANGLES, 0, triangles.size() / 3);
            glDisableClientState(GL_VERTEX_ARRAY);            


            /*
            glBegin(GL_POLYGON);
            for (auto& p : face)
            {
                glVertex3f(p.x, p.y, p.z);
            }
            glEnd();
            */

            i++;
        }
        glPopMatrix();
    }

    if (drawAxes)
    {
        glPushMatrix();

        glutSolidSphere(.01f, 100, 100);

        //x
        glColor4f(0.0f, 0.3f, 0.0f, 1.5f);
        glBegin(GL_LINES);
        glVertex3f(-2, 0, 0);
        glVertex3f(2, 0, 0);

        //arrow
        glVertex3f(2.0, 0.0f, 0.0f);
        glVertex3f(1.8, 0.1f, 0.0f);
        glVertex3f(2.0, 0.0f, 0.0f);
        glVertex3f(1.8, -0.1f, 0.0f);

        glEnd();

        //y
        glColor4f(0.3f, 0.0f, 0.0f, 1.5f);
        glBegin(GL_LINES);
        glVertex3f(0, -2, 0);
        glVertex3f(0, 2, 0);

        //arrow
        glVertex3f(0.0f, 2.0f, 0.0f);
        glVertex3f(0.1f, 1.8f, 0.0f);
        glVertex3f(0.0f, 2.0f, 0.0f);
        glVertex3f(-0.1f, 1.8f, 0.0f);

        glEnd();

        //z
        glColor4f(0.0f, 0.0f, 0.3f, 1.5f);
        glBegin(GL_LINES);
        glVertex3f(0, 0, -2);
        glVertex3f(0, 0, 2);

        //arrow
        glVertex3f(0.0, 0.0f, -2.0f);
        glVertex3f(0.0, 0.1f, -1.8f);
        glVertex3f(0.0, 0.0f, -2.0f);
        glVertex3f(0.0, -0.1f, -1.8f);

        glEnd();

        glPopMatrix();
    }

    glPopMatrix();
}

void MouseCallback(int button, int state, int x, int y)
{
    mouse = { x, y, button, state };
}

void MouseMotionCallback(int x, int y)
{
    if ((mouse.button == GLUT_LEFT_BUTTON) && (mouse.state == GLUT_DOWN))
    {
        cameraAngleXY.first += (y - mouse.y) * 0.3f;
        cameraAngleXY.second += (x - mouse.x) * 0.3f;
        mouse.x = x;
        mouse.y = y;
    }
    else if ((mouse.button == GLUT_MIDDLE_BUTTON) && (mouse.state == GLUT_DOWN))
    {
        cameraDistance -= (y - mouse.y) * 0.1f;
        mouse.y = y;
    }

    glutPostRedisplay();
}

void KbCallBack(unsigned char key, int x, int y)
{
    switch (key)
    {
    case 's':
        save("test1.pdf");
        glPushMatrix();
        glRotatef(180, 0, 1, 0);
        save("test2.pdf");
        glPopMatrix();
        break;
    }
    glutPostRedisplay();
    std::cout << key;
}

void SpCallBack(int key, int x, int y)
{
    const auto mods = glutGetModifiers();

    if (GLUT_ACTIVE_CTRL & mods)
    {
        switch (key)
        {
        case GLUT_KEY_LEFT:
            cameraTransXY.first -= 0.5;
            break;
        case GLUT_KEY_RIGHT:
            cameraTransXY.first += 0.5;
            break;
        case GLUT_KEY_DOWN:
            cameraTransXY.second += 0.5;
            break;
        case GLUT_KEY_UP:
            cameraTransXY.second -= 0.5;
            break;
        case GLUT_KEY_PAGE_UP:
            break;

        }
    }
    else
    {

        switch (key)
        {
        case GLUT_KEY_LEFT:
            cameraAngleXY.second -= 0.5;
            break;
        case GLUT_KEY_RIGHT:
            cameraAngleXY.second += 0.5;
            break;
        case GLUT_KEY_DOWN:
            cameraAngleXY.first += 0.5;
            break;
        case GLUT_KEY_UP:
            cameraAngleXY.first -= 0.5;
            break;
        case GLUT_KEY_PAGE_UP:
            break;

        }
    }
    glutPostRedisplay();
    std::cout << key;
}

void ReshapeCallback(int w, int h)
{
    screenWH = { w, h };

    glViewport(0, 0, (GLsizei)screenWH.first, (GLsizei)screenWH.second);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();

    gluPerspective(45.0f, (float)(screenWH.first) / screenWH.second, 1.0f, 100.0f); // FOV, AspectRatio, NearClip, FarClip

    // switch to modelview matrix in order to set scene
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

void TimerCallback(int millisec)
{
    glutTimerFunc(millisec, TimerCallback, millisec);
    glutPostRedisplay();
}

void MenuCallback(int item)
{
    switch (item)
    {
    case 1:
        drawG = !drawG;
        break;
    case 2:
        drawG2 = !drawG2;
        break;
    case 3:
        drawSphere = !drawSphere;
        break;
    case 4:
        drawFaces = !drawFaces;
        break;
    case 5:
        drawColors = !drawColors;
        break;
    case 6:
        drawAxes = !drawAxes;
        break;
    case 7:
        drawPoints = !drawPoints;
        break;
    case 8:
        drawFacesSkeletons = !drawFacesSkeletons;
        break;
    default:
        break;
    }

    glutPostRedisplay();
}

int main(int argc, char *argv[])
{
    std::cout << "xyz: ";  std::cin >> fileName;
    std::cout << "colors: ";  std::cin >> nColors;

    points = readXYZ(fileName + ".xyz");
    edges = readTriangEdges(fileName + ".g");
    edges2 = readTriangEdges(fileName + ".g2");
    faces = readFaces(fileName + ".vor");
    coloring = readColoring(fileName + "." + nColors + "c");

    for (auto& f : faces)
    {
        faces2.push_back(upgrade_face(f));
    }

    sedges = std::set<std::pair<int, int>>(edges.begin(), edges.end());
    sedges2 = std::set<std::pair<int, int>>(edges2.begin(), edges2.end());
    std::set_difference(sedges2.begin(), sedges2.end(), sedges.begin(), sedges.end(),
        std::inserter(sedges3, sedges3.end()));

    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH | GLUT_STENCIL);
    glutInitWindowSize(1000, 800);
    glutInitWindowPosition(0, 0);
    glutCreateWindow((fileName + ".xyz").c_str());

    {
        glutDisplayFunc(DisplayCallback);
        glutMouseFunc(MouseCallback);
        glutMotionFunc(MouseMotionCallback);
        glutTimerFunc(100, TimerCallback, 100);
        glutSpecialFunc(SpCallBack);
        glutKeyboardUpFunc(KbCallBack);
        glutReshapeFunc(ReshapeCallback);        
    }

    {
        glClearColor(0, 0, 0, 0);
        glShadeModel(GL_SMOOTH);
        glEnable(GL_DEPTH_TEST);
        glEnable(GL_POINT_SMOOTH);
        glEnable(GL_LINE_SMOOTH);
        glEnable(GL_POLYGON_SMOOTH);
        //glEnable(GL_LIGHTING);
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST);
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST); 
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);        

        //glPointSize(point_size);
        //glLineWidth(line_width);
    }

    //light
    {
        GLfloat lightKa[] = { .3f, .3f, .3f, .9f };  // ambient light
        GLfloat lightKd[] = { .7f, .7f, .7f, .9f };  // diffuse light
        GLfloat lightKs[] = { .9f, .9f, .9f, .9f };   // specular light
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightKa);
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightKd);
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightKs);

        float lightPos[4] = { 0, 0, 1, 0 }; // directional light
        glLightfv(GL_LIGHT0, GL_POSITION, lightPos);
        glEnable(GL_LIGHT0);
    }

    //menu
    {
        glutCreateMenu(MenuCallback);
        glutAddMenuEntry("Show G", 1);
        glutAddMenuEntry("Show G2", 2);
        glutAddMenuEntry("Show sphere", 3);
        glutAddMenuEntry("Show faces", 4);
        glutAddMenuEntry("Show colors", 5);
        glutAddMenuEntry("Show axes", 6);
        glutAddMenuEntry("Show points", 7);
        glutAddMenuEntry("Show faces skeletpons", 8);
        glutAttachMenu(GLUT_RIGHT_BUTTON);
    }

    glutMainLoop();

    return 0;
}

