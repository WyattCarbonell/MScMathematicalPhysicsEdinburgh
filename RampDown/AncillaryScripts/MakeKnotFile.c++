#include<iostream>
#include<stdlib.h>
#include<cmath>
#include<sstream>
#include<fstream>
#include<string>
#include<iomanip>

using namespace std;

const double PI  = 3.141592653589793238462;

int k=0;
int Kmax;
int Kstart = 0;

const int Tmax=1000;
const int Nmax=1;
const int Nbeadsmax=1000;

int N,Nbeads;
int DeltaT=100;
double dt=0.01;
double Lx,Ly,Lz;

double Rg[Nmax];
double Rg2[Nmax];
double Rg4[Nmax];
double Rgave;
double Rg2ave;
double Rg4ave;

//Observables
double position[Nmax][Nbeadsmax][3];

int main(int argc, char* argv[]){
srand(time(NULL));

cout << "Write argv[1]: datain; argv[2] = dataout; argv[3]=Tmax; argv[4]=N; argv[5]=Nbeads; argv[6]=DeltaT"<< endl;
cout << "Num of files to convert:";
Kmax=int(atoi(argv[3]));
cout << Kmax <<endl;
cout << "Number of Polymers:";
N=int(atoi(argv[4]));
cout << N <<endl;
cout<<"Number of Beads in each polymer:";
Nbeads=int(atoi(argv[5]));
cout << Nbeads <<endl;
cout<<"DeltaT:";
DeltaT=int(atoi(argv[6]));
cout << DeltaT <<endl;

stringstream writeFileKN;
writeFileKN <<"KN_"<<argv[2];
ofstream writeKN(writeFileKN.str().c_str());

/////////////////////////////////////////////////////
//MAIN LOOP OVER TIME!!!
////////////////////////////////////////////////////
for(k=0;k<Kmax;k++){

ifstream indata;
stringstream readFile;
readFile.str("");
readFile.clear();
long long int sum = int((k+Kstart));
if(sum==0) readFile << argv[1] <<sum;
if(DeltaT==1)if(sum>0)readFile << argv[1] <<sum;
if(DeltaT==100)if(sum>0)readFile << argv[1] <<sum << "00";
if(DeltaT==1000)if(sum>0)readFile << argv[1] <<sum << "000";
if(DeltaT==10000)if(sum>0)readFile << argv[1] <<sum << "0000";
indata.open(readFile.str().c_str());
cout << readFile.str().c_str()<<endl;
if(!indata){cout <<"file "<< readFile.str().c_str() << " is not there"<<endl; return 0;}

long int id,type,mol;
double num1,num2,num3;
double x,y,z;
string dummy;
long long int time;
long int Ntot;
double l1,l2;

//read 10 lines
for(int i=0;i<10;i++){
if(i==1) {
indata >> time;
time = k*DeltaT*dt;
cout << "time " << time <<endl;
}
if(i==3) {
indata >> Ntot;
cout << "Ntot " << Ntot<<endl;
}
if(i==5) {
indata >> l1 >> l2;
cout << "L " << l1<< " " << l2 <<endl;
Lx = l2-l1;
cout << "Lx " << Lx <<endl;
}
if(i==6) {
indata >> l1 >> l2;
cout << "L " << l1<< " " << l2 <<endl;
Ly = l2-l1;
cout << "Ly " << Ly <<endl;
}
if(i==7) {
indata >> l1 >> l2;
cout << "L " << l1<< " " << l2 <<endl;
Lz = l2-l1;
cout << "Lz " << Lz<<endl;
}

else getline(indata,dummy);
cout << dummy<<endl;
}
 
//////////////////////////
//READ FILES
////////////////////////////
for(int n=0; n<Ntot; n++){

    //indata >> id>>  x>>y>>z>>num1>>num2>>num3;
    indata >> id>>type>>x>>y>>z>>num1>>num2>>num3;
    //cout << "type! " << type <<endl; cin.get();

    int Nring = floor((double)(id-1)/(1.0*Nbeads));
    
    position[Nring][(id-1)%Nbeads][0] = (x + Lx*num1);
    position[Nring][(id-1)%Nbeads][1] = (y + Ly*num2);
    position[Nring][(id-1)%Nbeads][2] = (z + Lz*num3);

}

//////////////////////////////
//WRITE KNOT file
////////////////////////////
int nr=0;
//ring
for(int nr=0;nr<N;nr++){
writeKN << Nbeads+1<< endl;
for(int n=0;n<Nbeads;n++)writeKN << position[nr][n][0] << " " << position[nr][n][1]<<" " << position[nr][n][2] <<endl;
writeKN<<position[nr][0][0]<<" "<<position[nr][0][1]<<" " <<position[nr][0][2]<<endl;
}
	
}//closes time (loop over k)


return 0 ;
}


