import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
plt.rcParams.update({"font.family":"serif","mathtext.fontset":"cm","font.size":11})
fig,ax=plt.subplots(figsize=(11,5.0)); ax.set_xlim(0,100); ax.set_ylim(0,52); ax.axis("off")
def box(x,y,w,h,fc="#ececec",lw=1.3):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0,rounding_size=1.2",fc=fc,ec="#222",lw=lw))
boxes=[(1,"Prop. 4.1–4.2","Delegation paradox",r"$v_i>g_i\ \rightarrow$ keep task human",r"(interior $x_i^{*}$ otherwise)"),
       (37,"Prop. 4.3","Bottleneck migration",r"$\partial S_i/\partial x_i=v_i-\tau_i>0$",r"$\rightarrow$ load moves to review"),
       (73,"Prop. 4.4","Governance–capacity",r"$\partial c^{*}/\partial f=\lambda k>0$",r"$\rightarrow$ friction sets staffing")]
W,H,Y=26,16,28
for x,a,b,c,d in boxes:
    box(x,Y,W,H); cx=x+W/2
    ax.text(cx,Y+12.6,a,ha="center",fontsize=12,fontweight="bold")
    ax.text(cx,Y+9.6,b,ha="center",fontsize=12,fontweight="bold")
    ax.text(cx,Y+5.6,c,ha="center",fontsize=10.5); ax.text(cx,Y+2.4,d,ha="center",fontsize=10.5)
    lx = x+7 if x>70 else cx
    ax.plot([lx,lx],[Y,10],color="#222",lw=1.2)
for x0,lab in [(27,"why humans\nkeep it"),(63,"so the firm\nmust hire")]:
    ax.add_patch(FancyArrowPatch((x0+0.8,Y+H/2),(x0+9.4,Y+H/2),arrowstyle="-|>",mutation_scale=18,lw=2.2,color="#333"))
    ax.text(x0+5,Y+H/2+2,lab,ha="center",va="bottom",fontsize=9.5,style="italic")
box(84,12.5,15,11,fc="#f4f4f4",lw=1.1)
ax.text(91.5,20.2,"Cor. 4.5",ha="center",fontsize=11.5,fontweight="bold")
ax.text(91.5,15.3,"interior optimal\n"+r"friction $f^{*}$",ha="center",fontsize=10,linespacing=1.3)
ax.plot([80,84],[18,18],color="#222",lw=1.1)
box(1,3,98,7,fc="#3a3a3a")
ax.text(50,6.5,r"verification cost $v_i(f)$ — decision parameter AND service-time component",ha="center",va="center",color="white",fontsize=12.5,fontweight="bold")
fig.savefig("../results/figures/CF3_causal_chain.pdf",bbox_inches="tight",pad_inches=0.05)
fig.savefig("../results/figures/CF3_causal_chain_v2.png",dpi=200,bbox_inches="tight",pad_inches=0.05)
