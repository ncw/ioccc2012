#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<inttypes.h>
#define H uint32_t
#define U uint64_t
#define N void
#define T int
#define P calloc(n,sizeof(U))
#define R return
#define I for(
#define M if(
#define E >>32
#define S i=0;i<n;i++)
                      U K=-(U)(H)-1,*B,*C
              ,*x,AC,h;T L,n,F,l,p,D,*_;U e(U x,U
           y){x=K-x;U r=y-x;M y<x)r+=K;R r;}U AB(U x,H
        w,U*c){U s=x+*c;H  t=s<x;*c=(s>>w)+(t<<(64-w));R
     s&((((U)1)<<w)-1             )  ;}  U Q(U x,U y ) {U r
   =x-y;M x<y)r+=K;R r;}                     U AD(U       b,U
  a){H d=b E,c=b;M a >=                      K)a-=           K;a=
  Q(a,c);a=Q(a,d) ;a=e                                         (a
 ,((U)c)<<32);R   a;}U A(                                        U
 x,U y){H a=x,b=  x E,c=y,d
 =y E;x=b*(U)c;y=a*(U)d;U e                                    =a*(
 U)c,f=b*(U)d,t;x+=y;M x<y)f                                   +=1LL
 <<32;t=x<<32;e+=t;M e<t)f+=                                    1;t=
 x E;f+=t;R AD(f,e);}U J(U                                     a,U b
 ){U r= 1;T i;I i=63;i>=0; i--){r=A(r,r);M(b            >>i)&1)r=A(r
  ,a);}R r;}U f(U a){R J(a,K            -2);}N G      (H n,U*x, U*y)
  {T i;I S x[i]=A(x[i],y[i     ]);}N g(   H n,U*x)    {T  i;I S x[i]
=A(x[i],x[i]);}N AA(){U d       = AC;           T k            ;I k=
F;k>=1;k--){T m=1<<k,c=m>>                      1,j,               r
;U w=1;I j=0;j<c;j++){I r=                     0;r<n              ;r
+=m){T a=r+j,b=a+c;U u=x[a]                   ,v=x[b]           ;x[a
]=e(u,v);x[b]=A(Q(u,v),w);}w=                 A(  w,d        );}d=A
(d,d);}}N W(){T k;I k=1;k<=F;k    ++         ){T m=1<<   k,   c=m>>
1,j,r;U z=(U)(1<<((H)F-(H)k)),    d=         J(h,z),w=1;I      j=0
;j<c;j++){I r=0;r<n;r+=m){T a   =r+j,   b=a+ c;U u=x[a], v=A   (w
,x[b]);x[a]=e(u,v);x[b]=Q(u,v);}w=A(w  ,d);}}}T O(){T o=0,i,  w=L
/n;U s=J(7,(K-1)/192/n*5);AC=J(s,192)   ;h=f  (AC   );M 2 *w  +F
>=61)R 0;l=w;D=1<<w;p=w+1;x=P;B=P;C=P;  _= P; *B=1;*C=f(  n);I
i=0;i<=n;i++){U t=(U)L*(U)i,r=t%n,b=t/n ;H               a;M r
E)R 0;M(H)r)b++;M b E)R 0;a=b;M i>0){U c=_[              i-1]
=a-o;M c!=w&&c!=w+1)R 0;M i<n){r=n-r;B[i]=J(s,r);C[i]= f(A(B
[i],n));}}o=a;}R 1;}U V(){T i=0,j=0;U r=0;I;i<64&&j<n;i+=_
[j],j++)r|=x[j]<<i;M r)R r;I r=j=0;j<n;j++)r|=x[j];R r;}
N X(H c,T i){while(c){I;i<n;i++){H y=1<<_[i];x[i]+=c;
M x[i]>=y)x[             i]-=y,c=1;            else
R;}i=0;}                     }N Y(H     c){T    i;
while(c)   {I S{H y=1<<        _[i]     ;x[i    ]-=
c;M x[i]>=y)x[i]+=y,c=1        ;else    R     ;}}}N
Z(U c){T i;while(c){I          S{x[    i]=AB(x[i],_[i],
&c);H t=c;M!(c E)&&t         <D){M t ) X(t,i+1);R;}}}}N q()
{T i;U c=0;G(n,x,         B);AA(F,x);g(n,x);W(F       ,x);G(n,x
,C);I S x[i]=          AB(x[i],_[i],&c);M c)Z(c);Y    (2);}T main(
T w,char**         v){T i,k,j;M w<2)       {puts("Usage: p [n]");R 1
;}L=atoi                       (v[1]       );j=w>2    ?atoi(v[2]):L-
2;do F++                       ,n=1<<F;while(!O          ());I k=0;k
<1;k++){*x=4;I i=0;i<j;i++)q();}printf("0x%016"PRIX64"\n",V());R 0;}

