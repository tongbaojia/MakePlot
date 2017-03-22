//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Tue Mar 21 19:43:32 2017 by ROOT version 6.04/16
// from TTree TinyTree/TinyTree
// found on file: hist-MiniNTuple.root
//////////////////////////////////////////////////////////

#ifndef TinyTree_h
#define TinyTree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class TinyTree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Float_t         runNumber;
   Float_t         lbNumber;
   Long64_t        eventNumber;
   Float_t         mHH;
   Float_t         mHH_pole;
   Float_t         detaHH;
   Float_t         dphiHH;
   Float_t         drHH;
   Float_t         j0_m;
   Float_t         j0_pt;
   Float_t         j0_eta;
   Float_t         j0_phi;
   Float_t         j0_nTrk;
   Float_t         j0_nb;
   Float_t         j0_trkdr;
   Float_t         j1_m;
   Float_t         j1_pt;
   Float_t         j1_eta;
   Float_t         j1_phi;
   Float_t         j1_nTrk;
   Float_t         j1_nb;
   Float_t         j1_trkdr;
   Float_t         j0_trk0_m;
   Float_t         j0_trk0_pt;
   Float_t         j0_trk0_eta;
   Float_t         j0_trk0_phi;
   Float_t         j0_trk0_Mv2;
   Float_t         j1_trk0_m;
   Float_t         j1_trk0_pt;
   Float_t         j1_trk0_eta;
   Float_t         j1_trk0_phi;
   Float_t         j1_trk0_Mv2;
   Float_t         j0_trk1_m;
   Float_t         j0_trk1_pt;
   Float_t         j0_trk1_eta;
   Float_t         j0_trk1_phi;
   Float_t         j0_trk1_Mv2;
   Float_t         j1_trk1_m;
   Float_t         j1_trk1_pt;
   Float_t         j1_trk1_eta;
   Float_t         j1_trk1_phi;
   Float_t         j1_trk1_Mv2;
   Float_t         Xzz;
   Float_t         Xww;
   Float_t         Xhh;
   Float_t         Rhh;
   Float_t         Xtt;
   Float_t         nresj;
   Float_t         weight;

   // List of branches
   TBranch        *b_runNumber;   //!
   TBranch        *b_lbNumber;   //!
   TBranch        *b_eventNumber;   //!
   TBranch        *b_mHH;   //!
   TBranch        *b_mHH_pole;   //!
   TBranch        *b_detaHH;   //!
   TBranch        *b_dphiHH;   //!
   TBranch        *b_drHH;   //!
   TBranch        *b_j0_m;   //!
   TBranch        *b_j0_pt;   //!
   TBranch        *b_j0_eta;   //!
   TBranch        *b_j0_phi;   //!
   TBranch        *b_j0_nTrk;   //!
   TBranch        *b_j0_nb;   //!
   TBranch        *b_j0_trkdr;   //!
   TBranch        *b_j1_m;   //!
   TBranch        *b_j1_pt;   //!
   TBranch        *b_j1_eta;   //!
   TBranch        *b_j1_phi;   //!
   TBranch        *b_j1_nTrk;   //!
   TBranch        *b_j1_nb;   //!
   TBranch        *b_j1_trkdr;   //!
   TBranch        *b_j0_trk0_m;   //!
   TBranch        *b_j0_trk0_pt;   //!
   TBranch        *b_j0_trk0_eta;   //!
   TBranch        *b_j0_trk0_phi;   //!
   TBranch        *b_j0_trk0_Mv2;   //!
   TBranch        *b_j1_trk0_m;   //!
   TBranch        *b_j1_trk0_pt;   //!
   TBranch        *b_j1_trk0_eta;   //!
   TBranch        *b_j1_trk0_phi;   //!
   TBranch        *b_j1_trk0_Mv2;   //!
   TBranch        *b_j0_trk1_m;   //!
   TBranch        *b_j0_trk1_pt;   //!
   TBranch        *b_j0_trk1_eta;   //!
   TBranch        *b_j0_trk1_phi;   //!
   TBranch        *b_j0_trk1_Mv2;   //!
   TBranch        *b_j1_trk1_m;   //!
   TBranch        *b_j1_trk1_pt;   //!
   TBranch        *b_j1_trk1_eta;   //!
   TBranch        *b_j1_trk1_phi;   //!
   TBranch        *b_j1_trk1_Mv2;   //!
   TBranch        *b_Xzz;   //!
   TBranch        *b_Xww;   //!
   TBranch        *b_Xhh;   //!
   TBranch        *b_Rhh;   //!
   TBranch        *b_Xtt;   //!
   TBranch        *b_nresj;   //!
   TBranch        *b_weight;   //!

   TinyTree(TTree *tree=0);
   virtual ~TinyTree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef TinyTree_cxx
TinyTree::TinyTree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("hist-MiniNTuple.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("hist-MiniNTuple.root");
      }
      f->GetObject("TinyTree",tree);

   }
   Init(tree);
}

TinyTree::~TinyTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t TinyTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t TinyTree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void TinyTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("lbNumber", &lbNumber, &b_lbNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("mHH", &mHH, &b_mHH);
   fChain->SetBranchAddress("mHH_pole", &mHH_pole, &b_mHH_pole);
   fChain->SetBranchAddress("detaHH", &detaHH, &b_detaHH);
   fChain->SetBranchAddress("dphiHH", &dphiHH, &b_dphiHH);
   fChain->SetBranchAddress("drHH", &drHH, &b_drHH);
   fChain->SetBranchAddress("j0_m", &j0_m, &b_j0_m);
   fChain->SetBranchAddress("j0_pt", &j0_pt, &b_j0_pt);
   fChain->SetBranchAddress("j0_eta", &j0_eta, &b_j0_eta);
   fChain->SetBranchAddress("j0_phi", &j0_phi, &b_j0_phi);
   fChain->SetBranchAddress("j0_nTrk", &j0_nTrk, &b_j0_nTrk);
   fChain->SetBranchAddress("j0_nb", &j0_nb, &b_j0_nb);
   fChain->SetBranchAddress("j0_trkdr", &j0_trkdr, &b_j0_trkdr);
   fChain->SetBranchAddress("j1_m", &j1_m, &b_j1_m);
   fChain->SetBranchAddress("j1_pt", &j1_pt, &b_j1_pt);
   fChain->SetBranchAddress("j1_eta", &j1_eta, &b_j1_eta);
   fChain->SetBranchAddress("j1_phi", &j1_phi, &b_j1_phi);
   fChain->SetBranchAddress("j1_nTrk", &j1_nTrk, &b_j1_nTrk);
   fChain->SetBranchAddress("j1_nb", &j1_nb, &b_j1_nb);
   fChain->SetBranchAddress("j1_trkdr", &j1_trkdr, &b_j1_trkdr);
   fChain->SetBranchAddress("j0_trk0_m", &j0_trk0_m, &b_j0_trk0_m);
   fChain->SetBranchAddress("j0_trk0_pt", &j0_trk0_pt, &b_j0_trk0_pt);
   fChain->SetBranchAddress("j0_trk0_eta", &j0_trk0_eta, &b_j0_trk0_eta);
   fChain->SetBranchAddress("j0_trk0_phi", &j0_trk0_phi, &b_j0_trk0_phi);
   fChain->SetBranchAddress("j0_trk0_Mv2", &j0_trk0_Mv2, &b_j0_trk0_Mv2);
   fChain->SetBranchAddress("j1_trk0_m", &j1_trk0_m, &b_j1_trk0_m);
   fChain->SetBranchAddress("j1_trk0_pt", &j1_trk0_pt, &b_j1_trk0_pt);
   fChain->SetBranchAddress("j1_trk0_eta", &j1_trk0_eta, &b_j1_trk0_eta);
   fChain->SetBranchAddress("j1_trk0_phi", &j1_trk0_phi, &b_j1_trk0_phi);
   fChain->SetBranchAddress("j1_trk0_Mv2", &j1_trk0_Mv2, &b_j1_trk0_Mv2);
   fChain->SetBranchAddress("j0_trk1_m", &j0_trk1_m, &b_j0_trk1_m);
   fChain->SetBranchAddress("j0_trk1_pt", &j0_trk1_pt, &b_j0_trk1_pt);
   fChain->SetBranchAddress("j0_trk1_eta", &j0_trk1_eta, &b_j0_trk1_eta);
   fChain->SetBranchAddress("j0_trk1_phi", &j0_trk1_phi, &b_j0_trk1_phi);
   fChain->SetBranchAddress("j0_trk1_Mv2", &j0_trk1_Mv2, &b_j0_trk1_Mv2);
   fChain->SetBranchAddress("j1_trk1_m", &j1_trk1_m, &b_j1_trk1_m);
   fChain->SetBranchAddress("j1_trk1_pt", &j1_trk1_pt, &b_j1_trk1_pt);
   fChain->SetBranchAddress("j1_trk1_eta", &j1_trk1_eta, &b_j1_trk1_eta);
   fChain->SetBranchAddress("j1_trk1_phi", &j1_trk1_phi, &b_j1_trk1_phi);
   fChain->SetBranchAddress("j1_trk1_Mv2", &j1_trk1_Mv2, &b_j1_trk1_Mv2);
   fChain->SetBranchAddress("Xzz", &Xzz, &b_Xzz);
   //fChain->SetBranchAddress("Xww", &Xww, &b_Xww);
   fChain->SetBranchAddress("Xhh", &Xhh, &b_Xhh);
   fChain->SetBranchAddress("Rhh", &Rhh, &b_Rhh);
   //fChain->SetBranchAddress("Xtt", &Xtt, &b_Xtt);
   fChain->SetBranchAddress("nresj", &nresj, &b_nresj);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   Notify();
}

Bool_t TinyTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void TinyTree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t TinyTree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef TinyTree_cxx
