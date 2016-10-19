//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Oct 19 14:00:41 2016 by ROOT version 6.07/01
// from TTree XhhMiniNtuple/XhhMiniNtuple
// found on file: group.phys-exotics.mc15_13TeV.301500.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1500.hh4b-02-00-00_MiniNTuple.root_skim
//////////////////////////////////////////////////////////

#ifndef MiniTree_h
#define MiniTree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include "vector"
#include "vector"
#include "vector"
#include "vector"
#include "vector"

class MiniTree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           runNumber;
   Long64_t        eventNumber;
   Int_t           lumiBlock;
   UInt_t          coreFlags;
   Int_t           mcEventNumber;
   Int_t           mcChannelNumber;
   Float_t         mcEventWeight;
   Int_t           NPV;
   Float_t         actualInteractionsPerCrossing;
   Float_t         averageInteractionsPerCrossing;
   Float_t         weight_pileup;
   Float_t         correct_mu;
   Int_t           rand_run_nr;
   Int_t           rand_lumiblock_nr;
   vector<string>  *passedTriggers;
   vector<float>   *triggerPrescales;
   Int_t           nresolvedJetss;
   vector<float>   *resolvedJets_E;
   vector<float>   *resolvedJets_pt;
   vector<float>   *resolvedJets_phi;
   vector<float>   *resolvedJets_eta;
   vector<float>   *resolvedJets_Timing;
   vector<float>   *resolvedJets_LArQuality;
   vector<float>   *resolvedJets_HECQuality;
   vector<float>   *resolvedJets_NegativeE;
   vector<float>   *resolvedJets_AverageLArQF;
   vector<float>   *resolvedJets_BchCorrCell;
   vector<float>   *resolvedJets_N90Constituents;
   vector<float>   *resolvedJets_LArBadHVEnergyFrac;
   vector<int>     *resolvedJets_LArBadHVNCell;
   vector<float>   *resolvedJets_OotFracClusters5;
   vector<float>   *resolvedJets_OotFracClusters10;
   vector<float>   *resolvedJets_LeadingClusterPt;
   vector<float>   *resolvedJets_LeadingClusterSecondLambda;
   vector<float>   *resolvedJets_LeadingClusterCenterLambda;
   vector<float>   *resolvedJets_LeadingClusterSecondR;
   vector<int>     *resolvedJets_clean_passLooseBad;
   vector<int>     *resolvedJets_clean_passLooseBadUgly;
   vector<int>     *resolvedJets_clean_passTightBad;
   vector<int>     *resolvedJets_clean_passTightBadUgly;
   vector<float>   *resolvedJets_NumTrkPt1000PV;
   vector<float>   *resolvedJets_SumPtTrkPt1000PV;
   vector<float>   *resolvedJets_TrackWidthPt1000PV;
   vector<float>   *resolvedJets_NumTrkPt500PV;
   vector<float>   *resolvedJets_SumPtTrkPt500PV;
   vector<float>   *resolvedJets_TrackWidthPt500PV;
   vector<float>   *resolvedJets_JVFPV;
   vector<float>   *resolvedJets_Jvt;
   vector<float>   *resolvedJets_JvtJvfcorr;
   vector<float>   *resolvedJets_JvtRpt;
   vector<vector<float> > *resolvedJets_JvtEff_SF_Loose;
   vector<vector<float> > *resolvedJets_JvtEff_SF_Medium;
   vector<vector<float> > *resolvedJets_JvtEff_SF_Tight;
   vector<float>   *resolvedJets_MV2c00;
   vector<float>   *resolvedJets_MV2c10;
   vector<float>   *resolvedJets_MV2c20;
   vector<int>     *resolvedJets_HadronConeExclTruthLabelID;
   vector<double>  *resolvedJets_JetVertexCharge_discriminant;
   Int_t           nresolvedJetss_Fix70;
   vector<int>     *resolvedJets_isFix70;
   vector<vector<float> > *resolvedJets_SFFix70;
   vector<float>   *weight_resolvedJetsSFFix70;
   Int_t           nboostedJetss;
   vector<float>   *boostedJets_E;
   vector<float>   *boostedJets_pt;
   vector<float>   *boostedJets_phi;
   vector<float>   *boostedJets_eta;
   vector<float>   *boostedJets__HECFrac;
   vector<float>   *boostedJets__EMFrac;
   vector<float>   *boostedJets__CentroidR;
   vector<float>   *boostedJets__FracSamplingMax;
   vector<float>   *boostedJets__FracSamplingMaxIndex;
   vector<float>   *boostedJets__LowEtConstituentsFrac;
   vector<float>   *boostedJets__GhostMuonSegmentCount;
   vector<float>   *boostedJets__Width;
   vector<vector<int> > *boostedJets_NumTrkPt1000;
   vector<vector<float> > *boostedJets_SumPtTrkPt1000;
   vector<vector<float> > *boostedJets_TrackWidthPt1000;
   vector<vector<int> > *boostedJets_NumTrkPt500;
   vector<vector<float> > *boostedJets_SumPtTrkPt500;
   vector<vector<float> > *boostedJets_TrackWidthPt500;
   vector<vector<float> > *boostedJets_JVF;
   Int_t           nlepTopJetss;
   vector<float>   *lepTopJets_E;
   vector<float>   *lepTopJets_pt;
   vector<float>   *lepTopJets_phi;
   vector<float>   *lepTopJets_eta;
   vector<float>   *lepTopJets_Timing;
   vector<float>   *lepTopJets_LArQuality;
   vector<float>   *lepTopJets_HECQuality;
   vector<float>   *lepTopJets_NegativeE;
   vector<float>   *lepTopJets_AverageLArQF;
   vector<float>   *lepTopJets_BchCorrCell;
   vector<float>   *lepTopJets_N90Constituents;
   vector<float>   *lepTopJets_LArBadHVEnergyFrac;
   vector<int>     *lepTopJets_LArBadHVNCell;
   vector<float>   *lepTopJets_OotFracClusters5;
   vector<float>   *lepTopJets_OotFracClusters10;
   vector<float>   *lepTopJets_LeadingClusterPt;
   vector<float>   *lepTopJets_LeadingClusterSecondLambda;
   vector<float>   *lepTopJets_LeadingClusterCenterLambda;
   vector<float>   *lepTopJets_LeadingClusterSecondR;
   vector<int>     *lepTopJets_clean_passLooseBad;
   vector<int>     *lepTopJets_clean_passLooseBadUgly;
   vector<int>     *lepTopJets_clean_passTightBad;
   vector<int>     *lepTopJets_clean_passTightBadUgly;
   vector<float>   *lepTopJets_NumTrkPt1000PV;
   vector<float>   *lepTopJets_SumPtTrkPt1000PV;
   vector<float>   *lepTopJets_TrackWidthPt1000PV;
   vector<float>   *lepTopJets_NumTrkPt500PV;
   vector<float>   *lepTopJets_SumPtTrkPt500PV;
   vector<float>   *lepTopJets_TrackWidthPt500PV;
   vector<float>   *lepTopJets_JVFPV;
   vector<float>   *lepTopJets_Jvt;
   vector<float>   *lepTopJets_JvtJvfcorr;
   vector<float>   *lepTopJets_JvtRpt;
   vector<vector<float> > *lepTopJets_JvtEff_SF_Loose;
   vector<vector<float> > *lepTopJets_JvtEff_SF_Medium;
   vector<vector<float> > *lepTopJets_JvtEff_SF_Tight;
   vector<float>   *lepTopJets_MV2c00;
   vector<float>   *lepTopJets_MV2c10;
   vector<float>   *lepTopJets_MV2c20;
   vector<int>     *lepTopJets_HadronConeExclTruthLabelID;
   Int_t           nlepTopJetss_Fix70;
   vector<int>     *lepTopJets_isFix70;
   vector<vector<float> > *lepTopJets_SFFix70;
   vector<float>   *weight_lepTopJetsSFFix70;
   Int_t           nmuon;
   vector<float>   *muon_m;
   vector<float>   *muon_pt;
   vector<float>   *muon_phi;
   vector<float>   *muon_eta;
   vector<int>     *muon_isIsolated_LooseTrackOnly;
   vector<int>     *muon_isIsolated_Loose;
   vector<int>     *muon_isIsolated_Tight;
   vector<int>     *muon_isIsolated_Gradient;
   vector<int>     *muon_isIsolated_GradientLoose;
   vector<int>     *muon_isIsolated_FixedCutLoose;
   vector<int>     *muon_isIsolated_FixedCutTightTrackOnly;
   vector<int>     *muon_isIsolated_UserDefinedFixEfficiency;
   vector<int>     *muon_isIsolated_UserDefinedCut;
   vector<float>   *muon_ptcone20;
   vector<float>   *muon_ptcone30;
   vector<float>   *muon_ptcone40;
   vector<float>   *muon_ptvarcone20;
   vector<float>   *muon_ptvarcone30;
   vector<float>   *muon_ptvarcone40;
   vector<float>   *muon_topoetcone20;
   vector<float>   *muon_topoetcone30;
   vector<float>   *muon_topoetcone40;
   vector<int>     *muon_isVeryLoose;
   vector<int>     *muon_isLoose;
   vector<int>     *muon_isMedium;
   vector<int>     *muon_isTight;
   vector<float>   *muon_EnergyLoss;
   vector<float>   *muon_EnergyLossSigma;
   vector<unsigned char> *muon_energyLossType;
   vector<float>   *muon_MeasEnergyLoss;
   vector<float>   *muon_MeasEnergyLossSigma;
   vector<float>   *muon_ParamEnergyLoss;
   vector<float>   *muon_ParamEnergyLossSigmaMinus;
   vector<float>   *muon_ParamEnergyLossSigmaPlus;
   Float_t         metFinalClus;
   Float_t         metFinalClusPx;
   Float_t         metFinalClusPy;
   Float_t         metFinalClusSumEt;
   Float_t         metFinalClusPhi;
   Float_t         metFinalTrk;
   Float_t         metFinalTrkPx;
   Float_t         metFinalTrkPy;
   Float_t         metFinalTrkSumEt;
   Float_t         metFinalTrkPhi;
   Int_t           ntruths;
   vector<float>   *truth_E;
   vector<float>   *truth_pt;
   vector<float>   *truth_phi;
   vector<float>   *truth_eta;
   vector<int>     *truth_pdgId;
   vector<int>     *truth_status;
   vector<int>     *truth_barcode;
   vector<int>     *truth_is_higgs;
   vector<int>     *truth_is_bhad;
   vector<float>   *truth_Bdecay_x;
   vector<float>   *truth_Bdecay_y;
   vector<float>   *truth_Bdecay_z;
   vector<int>     *truth_nParents;
   vector<vector<int> > *truth_parent_pdgId;
   vector<vector<int> > *truth_parent_barcode;
   vector<vector<int> > *truth_parent_status;
   vector<int>     *truth_nChildren;
   vector<vector<int> > *truth_child_pdgId;
   vector<vector<int> > *truth_child_barcode;
   vector<vector<int> > *truth_child_status;
   Double_t        truth_mtt;
   Bool_t          EventPass_XhhL1;
   Bool_t          EventPass_XhhHLT;
   Bool_t          EventPass_XhhTrig;
   Int_t           hcand_resolved_n;
   vector<float>   *hcand_resolved_pt;
   vector<float>   *hcand_resolved_eta;
   vector<float>   *hcand_resolved_phi;
   vector<float>   *hcand_resolved_m;
   vector<float>   *hcand_resolved_dRjj;
   vector<vector<int> > *jet_ak4emtopo_asso_idx_in_resolvedJets;
   vector<float>   *lepTop_pt;
   vector<float>   *lepTop_eta;
   vector<float>   *lepTop_phi;
   vector<float>   *lepTop_m;
   vector<float>   *lepTop_dRmj;
   vector<int>     *leptop_jet_idx_in_lepTopJets;
   vector<float>   *leptop_muon_pt;
   vector<float>   *leptop_muon_eta;
   vector<float>   *leptop_muon_phi;
   vector<float>   *leptop_muon_m;
   vector<float>   *leptop_muon_ptcone20;
   vector<float>   *leptop_met;
   vector<float>   *leptop_metphi;
   vector<float>   *leptop_dPhimmet;
   vector<float>   *leptop_Mt;
   Int_t           hcand_boosted_n;
   vector<float>   *hcand_boosted_pt;
   vector<float>   *hcand_boosted_eta;
   vector<float>   *hcand_boosted_phi;
   vector<float>   *hcand_boosted_m;
   vector<int>     *hcand_boosted_htag_loose;
   vector<int>     *hcand_boosted_htag_medium;
   vector<int>     *hcand_boosted_htag_tight;
   vector<int>     *hcand_boosted_Wtag_medium;
   vector<int>     *hcand_boosted_Ztag_medium;
   vector<int>     *hcand_boosted_Wtag_tight;
   vector<int>     *hcand_boosted_Ztag_tight;
   vector<float>   *hcand_boosted_dRjj;
   vector<float>   *hcand_boosted_D2;
   vector<float>   *hcand_boosted_Tau21;
   vector<float>   *hcand_boosted_Tau21WTA;
   vector<int>     *hcand_boosted_nTrack;
   vector<int>     *hcand_boosted_nHBosons;
   vector<int>     *hcand_boosted_nWBosons;
   vector<int>     *hcand_boosted_nZBosons;
   vector<int>     *jet_ak2track_asso_n;
   vector<int>     *jet_ak2track_asso_n_addl;
   vector<vector<float> > *jet_ak2track_asso_pt;
   vector<vector<float> > *jet_ak2track_asso_eta;
   vector<vector<float> > *jet_ak2track_asso_phi;
   vector<vector<float> > *jet_ak2track_asso_m;
   vector<vector<float> > *jet_ak2track_asso_MV2c00;
   vector<vector<float> > *jet_ak2track_asso_MV2c10;
   vector<vector<float> > *jet_ak2track_asso_MV2c20;
   vector<vector<float> > *jet_ak2track_asso_MV2c100;
   vector<vector<vector<float> > > *jet_ak2track_asso_sys;
   vector<string>  *jet_ak2track_asso_sysname;
   vector<float>   *boosted_bevent_sys;
   Int_t           truth_hcand_boosted_n;
   vector<int>     *truth_hcand_boosted_match;
   vector<float>   *truth_hcand_boosted_pt;
   vector<float>   *truth_hcand_boosted_eta;
   vector<float>   *truth_hcand_boosted_phi;
   vector<float>   *truth_hcand_boosted_m;
   Float_t         weight;
   Float_t         weight_xs;

   // List of branches
   TBranch        *b_runNumber;   //!
   TBranch        *b_eventNumber;   //!
   TBranch        *b_lumiBlock;   //!
   TBranch        *b_coreFlags;   //!
   TBranch        *b_mcEventNumber;   //!
   TBranch        *b_mcChannelNumber;   //!
   TBranch        *b_mcEventWeight;   //!
   TBranch        *b_NPV;   //!
   TBranch        *b_actualInteractionsPerCrossing;   //!
   TBranch        *b_averageInteractionsPerCrossing;   //!
   TBranch        *b_weight_pileup;   //!
   TBranch        *b_correct_mu;   //!
   TBranch        *b_rand_run_nr;   //!
   TBranch        *b_rand_lumiblock_nr;   //!
   TBranch        *b_passedTriggers;   //!
   TBranch        *b_triggerPrescales;   //!
   TBranch        *b_nresolvedJetss;   //!
   TBranch        *b_resolvedJets_E;   //!
   TBranch        *b_resolvedJets_pt;   //!
   TBranch        *b_resolvedJets_phi;   //!
   TBranch        *b_resolvedJets_eta;   //!
   TBranch        *b_resolvedJets_Timing;   //!
   TBranch        *b_resolvedJets_LArQuality;   //!
   TBranch        *b_resolvedJets_HECQuality;   //!
   TBranch        *b_resolvedJets_NegativeE;   //!
   TBranch        *b_resolvedJets_AverageLArQF;   //!
   TBranch        *b_resolvedJets_BchCorrCell;   //!
   TBranch        *b_resolvedJets_N90Constituents;   //!
   TBranch        *b_resolvedJets_LArBadHVEnergyFrac;   //!
   TBranch        *b_resolvedJets_LArBadHVNCell;   //!
   TBranch        *b_resolvedJets_OotFracClusters5;   //!
   TBranch        *b_resolvedJets_OotFracClusters10;   //!
   TBranch        *b_resolvedJets_LeadingClusterPt;   //!
   TBranch        *b_resolvedJets_LeadingClusterSecondLambda;   //!
   TBranch        *b_resolvedJets_LeadingClusterCenterLambda;   //!
   TBranch        *b_resolvedJets_LeadingClusterSecondR;   //!
   TBranch        *b_resolvedJets_clean_passLooseBad;   //!
   TBranch        *b_resolvedJets_clean_passLooseBadUgly;   //!
   TBranch        *b_resolvedJets_clean_passTightBad;   //!
   TBranch        *b_resolvedJets_clean_passTightBadUgly;   //!
   TBranch        *b_resolvedJets_NumTrkPt1000PV;   //!
   TBranch        *b_resolvedJets_SumPtTrkPt1000PV;   //!
   TBranch        *b_resolvedJets_TrackWidthPt1000PV;   //!
   TBranch        *b_resolvedJets_NumTrkPt500PV;   //!
   TBranch        *b_resolvedJets_SumPtTrkPt500PV;   //!
   TBranch        *b_resolvedJets_TrackWidthPt500PV;   //!
   TBranch        *b_resolvedJets_JVFPV;   //!
   TBranch        *b_resolvedJets_Jvt;   //!
   TBranch        *b_resolvedJets_JvtJvfcorr;   //!
   TBranch        *b_resolvedJets_JvtRpt;   //!
   TBranch        *b_resolvedJets_JvtEff_SF_Loose;   //!
   TBranch        *b_resolvedJets_JvtEff_SF_Medium;   //!
   TBranch        *b_resolvedJets_JvtEff_SF_Tight;   //!
   TBranch        *b_resolvedJets_MV2c00;   //!
   TBranch        *b_resolvedJets_MV2c10;   //!
   TBranch        *b_resolvedJets_MV2c20;   //!
   TBranch        *b_resolvedJets_HadronConeExclTruthLabelID;   //!
   TBranch        *b_resolvedJets_JetVertexCharge_discriminant;   //!
   TBranch        *b_nresolvedJetss_Fix70;   //!
   TBranch        *b_resolvedJets_isFix70;   //!
   TBranch        *b_resolvedJets_SFFix70;   //!
   TBranch        *b_weight_resolvedJetsSFFix70;   //!
   TBranch        *b_nboostedJetss;   //!
   TBranch        *b_boostedJets_E;   //!
   TBranch        *b_boostedJets_pt;   //!
   TBranch        *b_boostedJets_phi;   //!
   TBranch        *b_boostedJets_eta;   //!
   TBranch        *b_boostedJets__HECFrac;   //!
   TBranch        *b_boostedJets__EMFrac;   //!
   TBranch        *b_boostedJets__CentroidR;   //!
   TBranch        *b_boostedJets__FracSamplingMax;   //!
   TBranch        *b_boostedJets__FracSamplingMaxIndex;   //!
   TBranch        *b_boostedJets__LowEtConstituentsFrac;   //!
   TBranch        *b_boostedJets__GhostMuonSegmentCount;   //!
   TBranch        *b_boostedJets__Width;   //!
   TBranch        *b_boostedJets_NumTrkPt1000;   //!
   TBranch        *b_boostedJets_SumPtTrkPt1000;   //!
   TBranch        *b_boostedJets_TrackWidthPt1000;   //!
   TBranch        *b_boostedJets_NumTrkPt500;   //!
   TBranch        *b_boostedJets_SumPtTrkPt500;   //!
   TBranch        *b_boostedJets_TrackWidthPt500;   //!
   TBranch        *b_boostedJets_JVF;   //!
   TBranch        *b_nlepTopJetss;   //!
   TBranch        *b_lepTopJets_E;   //!
   TBranch        *b_lepTopJets_pt;   //!
   TBranch        *b_lepTopJets_phi;   //!
   TBranch        *b_lepTopJets_eta;   //!
   TBranch        *b_lepTopJets_Timing;   //!
   TBranch        *b_lepTopJets_LArQuality;   //!
   TBranch        *b_lepTopJets_HECQuality;   //!
   TBranch        *b_lepTopJets_NegativeE;   //!
   TBranch        *b_lepTopJets_AverageLArQF;   //!
   TBranch        *b_lepTopJets_BchCorrCell;   //!
   TBranch        *b_lepTopJets_N90Constituents;   //!
   TBranch        *b_lepTopJets_LArBadHVEnergyFrac;   //!
   TBranch        *b_lepTopJets_LArBadHVNCell;   //!
   TBranch        *b_lepTopJets_OotFracClusters5;   //!
   TBranch        *b_lepTopJets_OotFracClusters10;   //!
   TBranch        *b_lepTopJets_LeadingClusterPt;   //!
   TBranch        *b_lepTopJets_LeadingClusterSecondLambda;   //!
   TBranch        *b_lepTopJets_LeadingClusterCenterLambda;   //!
   TBranch        *b_lepTopJets_LeadingClusterSecondR;   //!
   TBranch        *b_lepTopJets_clean_passLooseBad;   //!
   TBranch        *b_lepTopJets_clean_passLooseBadUgly;   //!
   TBranch        *b_lepTopJets_clean_passTightBad;   //!
   TBranch        *b_lepTopJets_clean_passTightBadUgly;   //!
   TBranch        *b_lepTopJets_NumTrkPt1000PV;   //!
   TBranch        *b_lepTopJets_SumPtTrkPt1000PV;   //!
   TBranch        *b_lepTopJets_TrackWidthPt1000PV;   //!
   TBranch        *b_lepTopJets_NumTrkPt500PV;   //!
   TBranch        *b_lepTopJets_SumPtTrkPt500PV;   //!
   TBranch        *b_lepTopJets_TrackWidthPt500PV;   //!
   TBranch        *b_lepTopJets_JVFPV;   //!
   TBranch        *b_lepTopJets_Jvt;   //!
   TBranch        *b_lepTopJets_JvtJvfcorr;   //!
   TBranch        *b_lepTopJets_JvtRpt;   //!
   TBranch        *b_lepTopJets_JvtEff_SF_Loose;   //!
   TBranch        *b_lepTopJets_JvtEff_SF_Medium;   //!
   TBranch        *b_lepTopJets_JvtEff_SF_Tight;   //!
   TBranch        *b_lepTopJets_MV2c00;   //!
   TBranch        *b_lepTopJets_MV2c10;   //!
   TBranch        *b_lepTopJets_MV2c20;   //!
   TBranch        *b_lepTopJets_HadronConeExclTruthLabelID;   //!
   TBranch        *b_nlepTopJetss_Fix70;   //!
   TBranch        *b_lepTopJets_isFix70;   //!
   TBranch        *b_lepTopJets_SFFix70;   //!
   TBranch        *b_weight_lepTopJetsSFFix70;   //!
   TBranch        *b_nmuon;   //!
   TBranch        *b_muon_m;   //!
   TBranch        *b_muon_pt;   //!
   TBranch        *b_muon_phi;   //!
   TBranch        *b_muon_eta;   //!
   TBranch        *b_muon_isIsolated_LooseTrackOnly;   //!
   TBranch        *b_muon_isIsolated_Loose;   //!
   TBranch        *b_muon_isIsolated_Tight;   //!
   TBranch        *b_muon_isIsolated_Gradient;   //!
   TBranch        *b_muon_isIsolated_GradientLoose;   //!
   TBranch        *b_muon_isIsolated_FixedCutLoose;   //!
   TBranch        *b_muon_isIsolated_FixedCutTightTrackOnly;   //!
   TBranch        *b_muon_isIsolated_UserDefinedFixEfficiency;   //!
   TBranch        *b_muon_isIsolated_UserDefinedCut;   //!
   TBranch        *b_muon_ptcone20;   //!
   TBranch        *b_muon_ptcone30;   //!
   TBranch        *b_muon_ptcone40;   //!
   TBranch        *b_muon_ptvarcone20;   //!
   TBranch        *b_muon_ptvarcone30;   //!
   TBranch        *b_muon_ptvarcone40;   //!
   TBranch        *b_muon_topoetcone20;   //!
   TBranch        *b_muon_topoetcone30;   //!
   TBranch        *b_muon_topoetcone40;   //!
   TBranch        *b_muon_isVeryLoose;   //!
   TBranch        *b_muon_isLoose;   //!
   TBranch        *b_muon_isMedium;   //!
   TBranch        *b_muon_isTight;   //!
   TBranch        *b_muon_EnergyLoss;   //!
   TBranch        *b_muon_EnergyLossSigma;   //!
   TBranch        *b_muon_energyLossType;   //!
   TBranch        *b_muon_MeasEnergyLoss;   //!
   TBranch        *b_muon_MeasEnergyLossSigma;   //!
   TBranch        *b_muon_ParamEnergyLoss;   //!
   TBranch        *b_muon_ParamEnergyLossSigmaMinus;   //!
   TBranch        *b_muon_ParamEnergyLossSigmaPlus;   //!
   TBranch        *b_metFinalClus;   //!
   TBranch        *b_metFinalClusPx;   //!
   TBranch        *b_metFinalClusPy;   //!
   TBranch        *b_metFinalClusSumEt;   //!
   TBranch        *b_metFinalClusPhi;   //!
   TBranch        *b_metFinalTrk;   //!
   TBranch        *b_metFinalTrkPx;   //!
   TBranch        *b_metFinalTrkPy;   //!
   TBranch        *b_metFinalTrkSumEt;   //!
   TBranch        *b_metFinalTrkPhi;   //!
   TBranch        *b_ntruths;   //!
   TBranch        *b_truth_E;   //!
   TBranch        *b_truth_pt;   //!
   TBranch        *b_truth_phi;   //!
   TBranch        *b_truth_eta;   //!
   TBranch        *b_truth_pdgId;   //!
   TBranch        *b_truth_status;   //!
   TBranch        *b_truth_barcode;   //!
   TBranch        *b_truth_is_higgs;   //!
   TBranch        *b_truth_is_bhad;   //!
   TBranch        *b_truth_Bdecay_x;   //!
   TBranch        *b_truth_Bdecay_y;   //!
   TBranch        *b_truth_Bdecay_z;   //!
   TBranch        *b_truth_nParents;   //!
   TBranch        *b_truth_parent_pdgId;   //!
   TBranch        *b_truth_parent_barcode;   //!
   TBranch        *b_truth_parent_status;   //!
   TBranch        *b_truth_nChildren;   //!
   TBranch        *b_truth_child_pdgId;   //!
   TBranch        *b_truth_child_barcode;   //!
   TBranch        *b_truth_child_status;   //!
   TBranch        *b_truth_mtt;   //!
   TBranch        *b_EventPass_XhhL1;   //!
   TBranch        *b_EventPass_XhhHLT;   //!
   TBranch        *b_EventPass_XhhTrig;   //!
   TBranch        *b_hcand_resolved_n;   //!
   TBranch        *b_hcand_resolved_pt;   //!
   TBranch        *b_hcand_resolved_eta;   //!
   TBranch        *b_hcand_resolved_phi;   //!
   TBranch        *b_hcand_resolved_m;   //!
   TBranch        *b_hcand_resolved_dRjj;   //!
   TBranch        *b_jet_ak4emtopo_asso_idx_in_resolvedJets;   //!
   TBranch        *b_lepTop_pt;   //!
   TBranch        *b_lepTop_eta;   //!
   TBranch        *b_lepTop_phi;   //!
   TBranch        *b_lepTop_m;   //!
   TBranch        *b_lepTop_dRmj;   //!
   TBranch        *b_leptop_jet_idx_in_lepTopJets;   //!
   TBranch        *b_leptop_muon_pt;   //!
   TBranch        *b_leptop_muon_eta;   //!
   TBranch        *b_leptop_muon_phi;   //!
   TBranch        *b_leptop_muon_m;   //!
   TBranch        *b_leptop_muon_ptcone20;   //!
   TBranch        *b_leptop_met;   //!
   TBranch        *b_leptop_metphi;   //!
   TBranch        *b_leptop_dPhimmet;   //!
   TBranch        *b_leptop_Mt;   //!
   TBranch        *b_hcand_boosted_n;   //!
   TBranch        *b_hcand_boosted_pt;   //!
   TBranch        *b_hcand_boosted_eta;   //!
   TBranch        *b_hcand_boosted_phi;   //!
   TBranch        *b_hcand_boosted_m;   //!
   TBranch        *b_hcand_boosted_htag_loose;   //!
   TBranch        *b_hcand_boosted_htag_medium;   //!
   TBranch        *b_hcand_boosted_htag_tight;   //!
   TBranch        *b_hcand_boosted_Wtag_medium;   //!
   TBranch        *b_hcand_boosted_Ztag_medium;   //!
   TBranch        *b_hcand_boosted_Wtag_tight;   //!
   TBranch        *b_hcand_boosted_Ztag_tight;   //!
   TBranch        *b_hcand_boosted_dRjj;   //!
   TBranch        *b_hcand_boosted_D2;   //!
   TBranch        *b_hcand_boosted_Tau21;   //!
   TBranch        *b_hcand_boosted_Tau21WTA;   //!
   TBranch        *b_hcand_boosted_nTrack;   //!
   TBranch        *b_hcand_boosted_nHBosons;   //!
   TBranch        *b_hcand_boosted_nWBosons;   //!
   TBranch        *b_hcand_boosted_nZBosons;   //!
   TBranch        *b_jet_ak2track_asso_n;   //!
   TBranch        *b_jet_ak2track_asso_n_addl;   //!
   TBranch        *b_jet_ak2track_asso_pt;   //!
   TBranch        *b_jet_ak2track_asso_eta;   //!
   TBranch        *b_jet_ak2track_asso_phi;   //!
   TBranch        *b_jet_ak2track_asso_m;   //!
   TBranch        *b_jet_ak2track_asso_MV2c00;   //!
   TBranch        *b_jet_ak2track_asso_MV2c10;   //!
   TBranch        *b_jet_ak2track_asso_MV2c20;   //!
   TBranch        *b_jet_ak2track_asso_MV2c100;   //!
   TBranch        *b_jet_ak2track_asso_sys;   //!
   TBranch        *b_jet_ak2track_asso_sysname;   //!
   TBranch        *b_boosted_bevent_sys;   //!
   TBranch        *b_truth_hcand_boosted_n;   //!
   TBranch        *b_truth_hcand_boosted_match;   //!
   TBranch        *b_truth_hcand_boosted_pt;   //!
   TBranch        *b_truth_hcand_boosted_eta;   //!
   TBranch        *b_truth_hcand_boosted_phi;   //!
   TBranch        *b_truth_hcand_boosted_m;   //!
   TBranch        *b_weight;   //!
   TBranch        *b_weight_xs;   //!

   MiniTree(TTree *tree=0);
   virtual ~MiniTree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef MiniTree_cxx
MiniTree::MiniTree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("group.phys-exotics.mc15_13TeV.301500.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1500.hh4b-02-00-00_MiniNTuple.root_skim");
      if (!f || !f->IsOpen()) {
         f = new TFile("group.phys-exotics.mc15_13TeV.301500.MadGraphPythia8EvtGen_A14NNPDF23LO_RS_G_hh_bbbb_c10_M1500.hh4b-02-00-00_MiniNTuple.root_skim");
      }
      f->GetObject("XhhMiniNtuple",tree);

   }
   Init(tree);
}

MiniTree::~MiniTree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t MiniTree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t MiniTree::LoadTree(Long64_t entry)
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

void MiniTree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   passedTriggers = 0;
   triggerPrescales = 0;
   resolvedJets_E = 0;
   resolvedJets_pt = 0;
   resolvedJets_phi = 0;
   resolvedJets_eta = 0;
   resolvedJets_Timing = 0;
   resolvedJets_LArQuality = 0;
   resolvedJets_HECQuality = 0;
   resolvedJets_NegativeE = 0;
   resolvedJets_AverageLArQF = 0;
   resolvedJets_BchCorrCell = 0;
   resolvedJets_N90Constituents = 0;
   resolvedJets_LArBadHVEnergyFrac = 0;
   resolvedJets_LArBadHVNCell = 0;
   resolvedJets_OotFracClusters5 = 0;
   resolvedJets_OotFracClusters10 = 0;
   resolvedJets_LeadingClusterPt = 0;
   resolvedJets_LeadingClusterSecondLambda = 0;
   resolvedJets_LeadingClusterCenterLambda = 0;
   resolvedJets_LeadingClusterSecondR = 0;
   resolvedJets_clean_passLooseBad = 0;
   resolvedJets_clean_passLooseBadUgly = 0;
   resolvedJets_clean_passTightBad = 0;
   resolvedJets_clean_passTightBadUgly = 0;
   resolvedJets_NumTrkPt1000PV = 0;
   resolvedJets_SumPtTrkPt1000PV = 0;
   resolvedJets_TrackWidthPt1000PV = 0;
   resolvedJets_NumTrkPt500PV = 0;
   resolvedJets_SumPtTrkPt500PV = 0;
   resolvedJets_TrackWidthPt500PV = 0;
   resolvedJets_JVFPV = 0;
   resolvedJets_Jvt = 0;
   resolvedJets_JvtJvfcorr = 0;
   resolvedJets_JvtRpt = 0;
   resolvedJets_JvtEff_SF_Loose = 0;
   resolvedJets_JvtEff_SF_Medium = 0;
   resolvedJets_JvtEff_SF_Tight = 0;
   resolvedJets_MV2c00 = 0;
   resolvedJets_MV2c10 = 0;
   resolvedJets_MV2c20 = 0;
   resolvedJets_HadronConeExclTruthLabelID = 0;
   resolvedJets_JetVertexCharge_discriminant = 0;
   resolvedJets_isFix70 = 0;
   resolvedJets_SFFix70 = 0;
   weight_resolvedJetsSFFix70 = 0;
   boostedJets_E = 0;
   boostedJets_pt = 0;
   boostedJets_phi = 0;
   boostedJets_eta = 0;
   boostedJets__HECFrac = 0;
   boostedJets__EMFrac = 0;
   boostedJets__CentroidR = 0;
   boostedJets__FracSamplingMax = 0;
   boostedJets__FracSamplingMaxIndex = 0;
   boostedJets__LowEtConstituentsFrac = 0;
   boostedJets__GhostMuonSegmentCount = 0;
   boostedJets__Width = 0;
   boostedJets_NumTrkPt1000 = 0;
   boostedJets_SumPtTrkPt1000 = 0;
   boostedJets_TrackWidthPt1000 = 0;
   boostedJets_NumTrkPt500 = 0;
   boostedJets_SumPtTrkPt500 = 0;
   boostedJets_TrackWidthPt500 = 0;
   boostedJets_JVF = 0;
   lepTopJets_E = 0;
   lepTopJets_pt = 0;
   lepTopJets_phi = 0;
   lepTopJets_eta = 0;
   lepTopJets_Timing = 0;
   lepTopJets_LArQuality = 0;
   lepTopJets_HECQuality = 0;
   lepTopJets_NegativeE = 0;
   lepTopJets_AverageLArQF = 0;
   lepTopJets_BchCorrCell = 0;
   lepTopJets_N90Constituents = 0;
   lepTopJets_LArBadHVEnergyFrac = 0;
   lepTopJets_LArBadHVNCell = 0;
   lepTopJets_OotFracClusters5 = 0;
   lepTopJets_OotFracClusters10 = 0;
   lepTopJets_LeadingClusterPt = 0;
   lepTopJets_LeadingClusterSecondLambda = 0;
   lepTopJets_LeadingClusterCenterLambda = 0;
   lepTopJets_LeadingClusterSecondR = 0;
   lepTopJets_clean_passLooseBad = 0;
   lepTopJets_clean_passLooseBadUgly = 0;
   lepTopJets_clean_passTightBad = 0;
   lepTopJets_clean_passTightBadUgly = 0;
   lepTopJets_NumTrkPt1000PV = 0;
   lepTopJets_SumPtTrkPt1000PV = 0;
   lepTopJets_TrackWidthPt1000PV = 0;
   lepTopJets_NumTrkPt500PV = 0;
   lepTopJets_SumPtTrkPt500PV = 0;
   lepTopJets_TrackWidthPt500PV = 0;
   lepTopJets_JVFPV = 0;
   lepTopJets_Jvt = 0;
   lepTopJets_JvtJvfcorr = 0;
   lepTopJets_JvtRpt = 0;
   lepTopJets_JvtEff_SF_Loose = 0;
   lepTopJets_JvtEff_SF_Medium = 0;
   lepTopJets_JvtEff_SF_Tight = 0;
   lepTopJets_MV2c00 = 0;
   lepTopJets_MV2c10 = 0;
   lepTopJets_MV2c20 = 0;
   lepTopJets_HadronConeExclTruthLabelID = 0;
   lepTopJets_isFix70 = 0;
   lepTopJets_SFFix70 = 0;
   weight_lepTopJetsSFFix70 = 0;
   muon_m = 0;
   muon_pt = 0;
   muon_phi = 0;
   muon_eta = 0;
   muon_isIsolated_LooseTrackOnly = 0;
   muon_isIsolated_Loose = 0;
   muon_isIsolated_Tight = 0;
   muon_isIsolated_Gradient = 0;
   muon_isIsolated_GradientLoose = 0;
   muon_isIsolated_FixedCutLoose = 0;
   muon_isIsolated_FixedCutTightTrackOnly = 0;
   muon_isIsolated_UserDefinedFixEfficiency = 0;
   muon_isIsolated_UserDefinedCut = 0;
   muon_ptcone20 = 0;
   muon_ptcone30 = 0;
   muon_ptcone40 = 0;
   muon_ptvarcone20 = 0;
   muon_ptvarcone30 = 0;
   muon_ptvarcone40 = 0;
   muon_topoetcone20 = 0;
   muon_topoetcone30 = 0;
   muon_topoetcone40 = 0;
   muon_isVeryLoose = 0;
   muon_isLoose = 0;
   muon_isMedium = 0;
   muon_isTight = 0;
   muon_EnergyLoss = 0;
   muon_EnergyLossSigma = 0;
   muon_energyLossType = 0;
   muon_MeasEnergyLoss = 0;
   muon_MeasEnergyLossSigma = 0;
   muon_ParamEnergyLoss = 0;
   muon_ParamEnergyLossSigmaMinus = 0;
   muon_ParamEnergyLossSigmaPlus = 0;
   truth_E = 0;
   truth_pt = 0;
   truth_phi = 0;
   truth_eta = 0;
   truth_pdgId = 0;
   truth_status = 0;
   truth_barcode = 0;
   truth_is_higgs = 0;
   truth_is_bhad = 0;
   truth_Bdecay_x = 0;
   truth_Bdecay_y = 0;
   truth_Bdecay_z = 0;
   truth_nParents = 0;
   truth_parent_pdgId = 0;
   truth_parent_barcode = 0;
   truth_parent_status = 0;
   truth_nChildren = 0;
   truth_child_pdgId = 0;
   truth_child_barcode = 0;
   truth_child_status = 0;
   hcand_resolved_pt = 0;
   hcand_resolved_eta = 0;
   hcand_resolved_phi = 0;
   hcand_resolved_m = 0;
   hcand_resolved_dRjj = 0;
   jet_ak4emtopo_asso_idx_in_resolvedJets = 0;
   lepTop_pt = 0;
   lepTop_eta = 0;
   lepTop_phi = 0;
   lepTop_m = 0;
   lepTop_dRmj = 0;
   leptop_jet_idx_in_lepTopJets = 0;
   leptop_muon_pt = 0;
   leptop_muon_eta = 0;
   leptop_muon_phi = 0;
   leptop_muon_m = 0;
   leptop_muon_ptcone20 = 0;
   leptop_met = 0;
   leptop_metphi = 0;
   leptop_dPhimmet = 0;
   leptop_Mt = 0;
   hcand_boosted_pt = 0;
   hcand_boosted_eta = 0;
   hcand_boosted_phi = 0;
   hcand_boosted_m = 0;
   hcand_boosted_htag_loose = 0;
   hcand_boosted_htag_medium = 0;
   hcand_boosted_htag_tight = 0;
   hcand_boosted_Wtag_medium = 0;
   hcand_boosted_Ztag_medium = 0;
   hcand_boosted_Wtag_tight = 0;
   hcand_boosted_Ztag_tight = 0;
   hcand_boosted_dRjj = 0;
   hcand_boosted_D2 = 0;
   hcand_boosted_Tau21 = 0;
   hcand_boosted_Tau21WTA = 0;
   hcand_boosted_nTrack = 0;
   hcand_boosted_nHBosons = 0;
   hcand_boosted_nWBosons = 0;
   hcand_boosted_nZBosons = 0;
   jet_ak2track_asso_n = 0;
   jet_ak2track_asso_n_addl = 0;
   jet_ak2track_asso_pt = 0;
   jet_ak2track_asso_eta = 0;
   jet_ak2track_asso_phi = 0;
   jet_ak2track_asso_m = 0;
   jet_ak2track_asso_MV2c00 = 0;
   jet_ak2track_asso_MV2c10 = 0;
   jet_ak2track_asso_MV2c20 = 0;
   jet_ak2track_asso_MV2c100 = 0;
   jet_ak2track_asso_sys = 0;
   jet_ak2track_asso_sysname = 0;
   boosted_bevent_sys = 0;
   truth_hcand_boosted_match = 0;
   truth_hcand_boosted_pt = 0;
   truth_hcand_boosted_eta = 0;
   truth_hcand_boosted_phi = 0;
   truth_hcand_boosted_m = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("runNumber", &runNumber, &b_runNumber);
   fChain->SetBranchAddress("eventNumber", &eventNumber, &b_eventNumber);
   fChain->SetBranchAddress("lumiBlock", &lumiBlock, &b_lumiBlock);
   fChain->SetBranchAddress("coreFlags", &coreFlags, &b_coreFlags);
   fChain->SetBranchAddress("mcEventNumber", &mcEventNumber, &b_mcEventNumber);
   fChain->SetBranchAddress("mcChannelNumber", &mcChannelNumber, &b_mcChannelNumber);
   fChain->SetBranchAddress("mcEventWeight", &mcEventWeight, &b_mcEventWeight);
   fChain->SetBranchAddress("NPV", &NPV, &b_NPV);
   fChain->SetBranchAddress("actualInteractionsPerCrossing", &actualInteractionsPerCrossing, &b_actualInteractionsPerCrossing);
   fChain->SetBranchAddress("averageInteractionsPerCrossing", &averageInteractionsPerCrossing, &b_averageInteractionsPerCrossing);
   fChain->SetBranchAddress("weight_pileup", &weight_pileup, &b_weight_pileup);
   fChain->SetBranchAddress("correct_mu", &correct_mu, &b_correct_mu);
   fChain->SetBranchAddress("rand_run_nr", &rand_run_nr, &b_rand_run_nr);
   fChain->SetBranchAddress("rand_lumiblock_nr", &rand_lumiblock_nr, &b_rand_lumiblock_nr);
   fChain->SetBranchAddress("passedTriggers", &passedTriggers, &b_passedTriggers);
   fChain->SetBranchAddress("triggerPrescales", &triggerPrescales, &b_triggerPrescales);
   fChain->SetBranchAddress("nresolvedJetss", &nresolvedJetss, &b_nresolvedJetss);
   fChain->SetBranchAddress("resolvedJets_E", &resolvedJets_E, &b_resolvedJets_E);
   fChain->SetBranchAddress("resolvedJets_pt", &resolvedJets_pt, &b_resolvedJets_pt);
   fChain->SetBranchAddress("resolvedJets_phi", &resolvedJets_phi, &b_resolvedJets_phi);
   fChain->SetBranchAddress("resolvedJets_eta", &resolvedJets_eta, &b_resolvedJets_eta);
   fChain->SetBranchAddress("resolvedJets_Timing", &resolvedJets_Timing, &b_resolvedJets_Timing);
   fChain->SetBranchAddress("resolvedJets_LArQuality", &resolvedJets_LArQuality, &b_resolvedJets_LArQuality);
   fChain->SetBranchAddress("resolvedJets_HECQuality", &resolvedJets_HECQuality, &b_resolvedJets_HECQuality);
   fChain->SetBranchAddress("resolvedJets_NegativeE", &resolvedJets_NegativeE, &b_resolvedJets_NegativeE);
   fChain->SetBranchAddress("resolvedJets_AverageLArQF", &resolvedJets_AverageLArQF, &b_resolvedJets_AverageLArQF);
   fChain->SetBranchAddress("resolvedJets_BchCorrCell", &resolvedJets_BchCorrCell, &b_resolvedJets_BchCorrCell);
   fChain->SetBranchAddress("resolvedJets_N90Constituents", &resolvedJets_N90Constituents, &b_resolvedJets_N90Constituents);
   fChain->SetBranchAddress("resolvedJets_LArBadHVEnergyFrac", &resolvedJets_LArBadHVEnergyFrac, &b_resolvedJets_LArBadHVEnergyFrac);
   fChain->SetBranchAddress("resolvedJets_LArBadHVNCell", &resolvedJets_LArBadHVNCell, &b_resolvedJets_LArBadHVNCell);
   fChain->SetBranchAddress("resolvedJets_OotFracClusters5", &resolvedJets_OotFracClusters5, &b_resolvedJets_OotFracClusters5);
   fChain->SetBranchAddress("resolvedJets_OotFracClusters10", &resolvedJets_OotFracClusters10, &b_resolvedJets_OotFracClusters10);
   fChain->SetBranchAddress("resolvedJets_LeadingClusterPt", &resolvedJets_LeadingClusterPt, &b_resolvedJets_LeadingClusterPt);
   fChain->SetBranchAddress("resolvedJets_LeadingClusterSecondLambda", &resolvedJets_LeadingClusterSecondLambda, &b_resolvedJets_LeadingClusterSecondLambda);
   fChain->SetBranchAddress("resolvedJets_LeadingClusterCenterLambda", &resolvedJets_LeadingClusterCenterLambda, &b_resolvedJets_LeadingClusterCenterLambda);
   fChain->SetBranchAddress("resolvedJets_LeadingClusterSecondR", &resolvedJets_LeadingClusterSecondR, &b_resolvedJets_LeadingClusterSecondR);
   fChain->SetBranchAddress("resolvedJets_clean_passLooseBad", &resolvedJets_clean_passLooseBad, &b_resolvedJets_clean_passLooseBad);
   fChain->SetBranchAddress("resolvedJets_clean_passLooseBadUgly", &resolvedJets_clean_passLooseBadUgly, &b_resolvedJets_clean_passLooseBadUgly);
   fChain->SetBranchAddress("resolvedJets_clean_passTightBad", &resolvedJets_clean_passTightBad, &b_resolvedJets_clean_passTightBad);
   fChain->SetBranchAddress("resolvedJets_clean_passTightBadUgly", &resolvedJets_clean_passTightBadUgly, &b_resolvedJets_clean_passTightBadUgly);
   fChain->SetBranchAddress("resolvedJets_NumTrkPt1000PV", &resolvedJets_NumTrkPt1000PV, &b_resolvedJets_NumTrkPt1000PV);
   fChain->SetBranchAddress("resolvedJets_SumPtTrkPt1000PV", &resolvedJets_SumPtTrkPt1000PV, &b_resolvedJets_SumPtTrkPt1000PV);
   fChain->SetBranchAddress("resolvedJets_TrackWidthPt1000PV", &resolvedJets_TrackWidthPt1000PV, &b_resolvedJets_TrackWidthPt1000PV);
   fChain->SetBranchAddress("resolvedJets_NumTrkPt500PV", &resolvedJets_NumTrkPt500PV, &b_resolvedJets_NumTrkPt500PV);
   fChain->SetBranchAddress("resolvedJets_SumPtTrkPt500PV", &resolvedJets_SumPtTrkPt500PV, &b_resolvedJets_SumPtTrkPt500PV);
   fChain->SetBranchAddress("resolvedJets_TrackWidthPt500PV", &resolvedJets_TrackWidthPt500PV, &b_resolvedJets_TrackWidthPt500PV);
   fChain->SetBranchAddress("resolvedJets_JVFPV", &resolvedJets_JVFPV, &b_resolvedJets_JVFPV);
   fChain->SetBranchAddress("resolvedJets_Jvt", &resolvedJets_Jvt, &b_resolvedJets_Jvt);
   fChain->SetBranchAddress("resolvedJets_JvtJvfcorr", &resolvedJets_JvtJvfcorr, &b_resolvedJets_JvtJvfcorr);
   fChain->SetBranchAddress("resolvedJets_JvtRpt", &resolvedJets_JvtRpt, &b_resolvedJets_JvtRpt);
   fChain->SetBranchAddress("resolvedJets_JvtEff_SF_Loose", &resolvedJets_JvtEff_SF_Loose, &b_resolvedJets_JvtEff_SF_Loose);
   fChain->SetBranchAddress("resolvedJets_JvtEff_SF_Medium", &resolvedJets_JvtEff_SF_Medium, &b_resolvedJets_JvtEff_SF_Medium);
   fChain->SetBranchAddress("resolvedJets_JvtEff_SF_Tight", &resolvedJets_JvtEff_SF_Tight, &b_resolvedJets_JvtEff_SF_Tight);
   fChain->SetBranchAddress("resolvedJets_MV2c00", &resolvedJets_MV2c00, &b_resolvedJets_MV2c00);
   fChain->SetBranchAddress("resolvedJets_MV2c10", &resolvedJets_MV2c10, &b_resolvedJets_MV2c10);
   fChain->SetBranchAddress("resolvedJets_MV2c20", &resolvedJets_MV2c20, &b_resolvedJets_MV2c20);
   fChain->SetBranchAddress("resolvedJets_HadronConeExclTruthLabelID", &resolvedJets_HadronConeExclTruthLabelID, &b_resolvedJets_HadronConeExclTruthLabelID);
   fChain->SetBranchAddress("resolvedJets_JetVertexCharge_discriminant", &resolvedJets_JetVertexCharge_discriminant, &b_resolvedJets_JetVertexCharge_discriminant);
   fChain->SetBranchAddress("nresolvedJetss_Fix70", &nresolvedJetss_Fix70, &b_nresolvedJetss_Fix70);
   fChain->SetBranchAddress("resolvedJets_isFix70", &resolvedJets_isFix70, &b_resolvedJets_isFix70);
   fChain->SetBranchAddress("resolvedJets_SFFix70", &resolvedJets_SFFix70, &b_resolvedJets_SFFix70);
   fChain->SetBranchAddress("weight_resolvedJetsSFFix70", &weight_resolvedJetsSFFix70, &b_weight_resolvedJetsSFFix70);
   fChain->SetBranchAddress("nboostedJetss", &nboostedJetss, &b_nboostedJetss);
   fChain->SetBranchAddress("boostedJets_E", &boostedJets_E, &b_boostedJets_E);
   fChain->SetBranchAddress("boostedJets_pt", &boostedJets_pt, &b_boostedJets_pt);
   fChain->SetBranchAddress("boostedJets_phi", &boostedJets_phi, &b_boostedJets_phi);
   fChain->SetBranchAddress("boostedJets_eta", &boostedJets_eta, &b_boostedJets_eta);
   fChain->SetBranchAddress("boostedJets__HECFrac", &boostedJets__HECFrac, &b_boostedJets__HECFrac);
   fChain->SetBranchAddress("boostedJets__EMFrac", &boostedJets__EMFrac, &b_boostedJets__EMFrac);
   fChain->SetBranchAddress("boostedJets__CentroidR", &boostedJets__CentroidR, &b_boostedJets__CentroidR);
   fChain->SetBranchAddress("boostedJets__FracSamplingMax", &boostedJets__FracSamplingMax, &b_boostedJets__FracSamplingMax);
   fChain->SetBranchAddress("boostedJets__FracSamplingMaxIndex", &boostedJets__FracSamplingMaxIndex, &b_boostedJets__FracSamplingMaxIndex);
   fChain->SetBranchAddress("boostedJets__LowEtConstituentsFrac", &boostedJets__LowEtConstituentsFrac, &b_boostedJets__LowEtConstituentsFrac);
   fChain->SetBranchAddress("boostedJets__GhostMuonSegmentCount", &boostedJets__GhostMuonSegmentCount, &b_boostedJets__GhostMuonSegmentCount);
   fChain->SetBranchAddress("boostedJets__Width", &boostedJets__Width, &b_boostedJets__Width);
   fChain->SetBranchAddress("boostedJets_NumTrkPt1000", &boostedJets_NumTrkPt1000, &b_boostedJets_NumTrkPt1000);
   fChain->SetBranchAddress("boostedJets_SumPtTrkPt1000", &boostedJets_SumPtTrkPt1000, &b_boostedJets_SumPtTrkPt1000);
   fChain->SetBranchAddress("boostedJets_TrackWidthPt1000", &boostedJets_TrackWidthPt1000, &b_boostedJets_TrackWidthPt1000);
   fChain->SetBranchAddress("boostedJets_NumTrkPt500", &boostedJets_NumTrkPt500, &b_boostedJets_NumTrkPt500);
   fChain->SetBranchAddress("boostedJets_SumPtTrkPt500", &boostedJets_SumPtTrkPt500, &b_boostedJets_SumPtTrkPt500);
   fChain->SetBranchAddress("boostedJets_TrackWidthPt500", &boostedJets_TrackWidthPt500, &b_boostedJets_TrackWidthPt500);
   fChain->SetBranchAddress("boostedJets_JVF", &boostedJets_JVF, &b_boostedJets_JVF);
   fChain->SetBranchAddress("nlepTopJetss", &nlepTopJetss, &b_nlepTopJetss);
   fChain->SetBranchAddress("lepTopJets_E", &lepTopJets_E, &b_lepTopJets_E);
   fChain->SetBranchAddress("lepTopJets_pt", &lepTopJets_pt, &b_lepTopJets_pt);
   fChain->SetBranchAddress("lepTopJets_phi", &lepTopJets_phi, &b_lepTopJets_phi);
   fChain->SetBranchAddress("lepTopJets_eta", &lepTopJets_eta, &b_lepTopJets_eta);
   fChain->SetBranchAddress("lepTopJets_Timing", &lepTopJets_Timing, &b_lepTopJets_Timing);
   fChain->SetBranchAddress("lepTopJets_LArQuality", &lepTopJets_LArQuality, &b_lepTopJets_LArQuality);
   fChain->SetBranchAddress("lepTopJets_HECQuality", &lepTopJets_HECQuality, &b_lepTopJets_HECQuality);
   fChain->SetBranchAddress("lepTopJets_NegativeE", &lepTopJets_NegativeE, &b_lepTopJets_NegativeE);
   fChain->SetBranchAddress("lepTopJets_AverageLArQF", &lepTopJets_AverageLArQF, &b_lepTopJets_AverageLArQF);
   fChain->SetBranchAddress("lepTopJets_BchCorrCell", &lepTopJets_BchCorrCell, &b_lepTopJets_BchCorrCell);
   fChain->SetBranchAddress("lepTopJets_N90Constituents", &lepTopJets_N90Constituents, &b_lepTopJets_N90Constituents);
   fChain->SetBranchAddress("lepTopJets_LArBadHVEnergyFrac", &lepTopJets_LArBadHVEnergyFrac, &b_lepTopJets_LArBadHVEnergyFrac);
   fChain->SetBranchAddress("lepTopJets_LArBadHVNCell", &lepTopJets_LArBadHVNCell, &b_lepTopJets_LArBadHVNCell);
   fChain->SetBranchAddress("lepTopJets_OotFracClusters5", &lepTopJets_OotFracClusters5, &b_lepTopJets_OotFracClusters5);
   fChain->SetBranchAddress("lepTopJets_OotFracClusters10", &lepTopJets_OotFracClusters10, &b_lepTopJets_OotFracClusters10);
   fChain->SetBranchAddress("lepTopJets_LeadingClusterPt", &lepTopJets_LeadingClusterPt, &b_lepTopJets_LeadingClusterPt);
   fChain->SetBranchAddress("lepTopJets_LeadingClusterSecondLambda", &lepTopJets_LeadingClusterSecondLambda, &b_lepTopJets_LeadingClusterSecondLambda);
   fChain->SetBranchAddress("lepTopJets_LeadingClusterCenterLambda", &lepTopJets_LeadingClusterCenterLambda, &b_lepTopJets_LeadingClusterCenterLambda);
   fChain->SetBranchAddress("lepTopJets_LeadingClusterSecondR", &lepTopJets_LeadingClusterSecondR, &b_lepTopJets_LeadingClusterSecondR);
   fChain->SetBranchAddress("lepTopJets_clean_passLooseBad", &lepTopJets_clean_passLooseBad, &b_lepTopJets_clean_passLooseBad);
   fChain->SetBranchAddress("lepTopJets_clean_passLooseBadUgly", &lepTopJets_clean_passLooseBadUgly, &b_lepTopJets_clean_passLooseBadUgly);
   fChain->SetBranchAddress("lepTopJets_clean_passTightBad", &lepTopJets_clean_passTightBad, &b_lepTopJets_clean_passTightBad);
   fChain->SetBranchAddress("lepTopJets_clean_passTightBadUgly", &lepTopJets_clean_passTightBadUgly, &b_lepTopJets_clean_passTightBadUgly);
   fChain->SetBranchAddress("lepTopJets_NumTrkPt1000PV", &lepTopJets_NumTrkPt1000PV, &b_lepTopJets_NumTrkPt1000PV);
   fChain->SetBranchAddress("lepTopJets_SumPtTrkPt1000PV", &lepTopJets_SumPtTrkPt1000PV, &b_lepTopJets_SumPtTrkPt1000PV);
   fChain->SetBranchAddress("lepTopJets_TrackWidthPt1000PV", &lepTopJets_TrackWidthPt1000PV, &b_lepTopJets_TrackWidthPt1000PV);
   fChain->SetBranchAddress("lepTopJets_NumTrkPt500PV", &lepTopJets_NumTrkPt500PV, &b_lepTopJets_NumTrkPt500PV);
   fChain->SetBranchAddress("lepTopJets_SumPtTrkPt500PV", &lepTopJets_SumPtTrkPt500PV, &b_lepTopJets_SumPtTrkPt500PV);
   fChain->SetBranchAddress("lepTopJets_TrackWidthPt500PV", &lepTopJets_TrackWidthPt500PV, &b_lepTopJets_TrackWidthPt500PV);
   fChain->SetBranchAddress("lepTopJets_JVFPV", &lepTopJets_JVFPV, &b_lepTopJets_JVFPV);
   fChain->SetBranchAddress("lepTopJets_Jvt", &lepTopJets_Jvt, &b_lepTopJets_Jvt);
   fChain->SetBranchAddress("lepTopJets_JvtJvfcorr", &lepTopJets_JvtJvfcorr, &b_lepTopJets_JvtJvfcorr);
   fChain->SetBranchAddress("lepTopJets_JvtRpt", &lepTopJets_JvtRpt, &b_lepTopJets_JvtRpt);
   fChain->SetBranchAddress("lepTopJets_JvtEff_SF_Loose", &lepTopJets_JvtEff_SF_Loose, &b_lepTopJets_JvtEff_SF_Loose);
   fChain->SetBranchAddress("lepTopJets_JvtEff_SF_Medium", &lepTopJets_JvtEff_SF_Medium, &b_lepTopJets_JvtEff_SF_Medium);
   fChain->SetBranchAddress("lepTopJets_JvtEff_SF_Tight", &lepTopJets_JvtEff_SF_Tight, &b_lepTopJets_JvtEff_SF_Tight);
   fChain->SetBranchAddress("lepTopJets_MV2c00", &lepTopJets_MV2c00, &b_lepTopJets_MV2c00);
   fChain->SetBranchAddress("lepTopJets_MV2c10", &lepTopJets_MV2c10, &b_lepTopJets_MV2c10);
   fChain->SetBranchAddress("lepTopJets_MV2c20", &lepTopJets_MV2c20, &b_lepTopJets_MV2c20);
   fChain->SetBranchAddress("lepTopJets_HadronConeExclTruthLabelID", &lepTopJets_HadronConeExclTruthLabelID, &b_lepTopJets_HadronConeExclTruthLabelID);
   fChain->SetBranchAddress("nlepTopJetss_Fix70", &nlepTopJetss_Fix70, &b_nlepTopJetss_Fix70);
   fChain->SetBranchAddress("lepTopJets_isFix70", &lepTopJets_isFix70, &b_lepTopJets_isFix70);
   fChain->SetBranchAddress("lepTopJets_SFFix70", &lepTopJets_SFFix70, &b_lepTopJets_SFFix70);
   fChain->SetBranchAddress("weight_lepTopJetsSFFix70", &weight_lepTopJetsSFFix70, &b_weight_lepTopJetsSFFix70);
   fChain->SetBranchAddress("nmuon", &nmuon, &b_nmuon);
   fChain->SetBranchAddress("muon_m", &muon_m, &b_muon_m);
   fChain->SetBranchAddress("muon_pt", &muon_pt, &b_muon_pt);
   fChain->SetBranchAddress("muon_phi", &muon_phi, &b_muon_phi);
   fChain->SetBranchAddress("muon_eta", &muon_eta, &b_muon_eta);
   fChain->SetBranchAddress("muon_isIsolated_LooseTrackOnly", &muon_isIsolated_LooseTrackOnly, &b_muon_isIsolated_LooseTrackOnly);
   fChain->SetBranchAddress("muon_isIsolated_Loose", &muon_isIsolated_Loose, &b_muon_isIsolated_Loose);
   fChain->SetBranchAddress("muon_isIsolated_Tight", &muon_isIsolated_Tight, &b_muon_isIsolated_Tight);
   fChain->SetBranchAddress("muon_isIsolated_Gradient", &muon_isIsolated_Gradient, &b_muon_isIsolated_Gradient);
   fChain->SetBranchAddress("muon_isIsolated_GradientLoose", &muon_isIsolated_GradientLoose, &b_muon_isIsolated_GradientLoose);
   fChain->SetBranchAddress("muon_isIsolated_FixedCutLoose", &muon_isIsolated_FixedCutLoose, &b_muon_isIsolated_FixedCutLoose);
   fChain->SetBranchAddress("muon_isIsolated_FixedCutTightTrackOnly", &muon_isIsolated_FixedCutTightTrackOnly, &b_muon_isIsolated_FixedCutTightTrackOnly);
   fChain->SetBranchAddress("muon_isIsolated_UserDefinedFixEfficiency", &muon_isIsolated_UserDefinedFixEfficiency, &b_muon_isIsolated_UserDefinedFixEfficiency);
   fChain->SetBranchAddress("muon_isIsolated_UserDefinedCut", &muon_isIsolated_UserDefinedCut, &b_muon_isIsolated_UserDefinedCut);
   fChain->SetBranchAddress("muon_ptcone20", &muon_ptcone20, &b_muon_ptcone20);
   fChain->SetBranchAddress("muon_ptcone30", &muon_ptcone30, &b_muon_ptcone30);
   fChain->SetBranchAddress("muon_ptcone40", &muon_ptcone40, &b_muon_ptcone40);
   fChain->SetBranchAddress("muon_ptvarcone20", &muon_ptvarcone20, &b_muon_ptvarcone20);
   fChain->SetBranchAddress("muon_ptvarcone30", &muon_ptvarcone30, &b_muon_ptvarcone30);
   fChain->SetBranchAddress("muon_ptvarcone40", &muon_ptvarcone40, &b_muon_ptvarcone40);
   fChain->SetBranchAddress("muon_topoetcone20", &muon_topoetcone20, &b_muon_topoetcone20);
   fChain->SetBranchAddress("muon_topoetcone30", &muon_topoetcone30, &b_muon_topoetcone30);
   fChain->SetBranchAddress("muon_topoetcone40", &muon_topoetcone40, &b_muon_topoetcone40);
   fChain->SetBranchAddress("muon_isVeryLoose", &muon_isVeryLoose, &b_muon_isVeryLoose);
   fChain->SetBranchAddress("muon_isLoose", &muon_isLoose, &b_muon_isLoose);
   fChain->SetBranchAddress("muon_isMedium", &muon_isMedium, &b_muon_isMedium);
   fChain->SetBranchAddress("muon_isTight", &muon_isTight, &b_muon_isTight);
   fChain->SetBranchAddress("muon_EnergyLoss", &muon_EnergyLoss, &b_muon_EnergyLoss);
   fChain->SetBranchAddress("muon_EnergyLossSigma", &muon_EnergyLossSigma, &b_muon_EnergyLossSigma);
   fChain->SetBranchAddress("muon_energyLossType", &muon_energyLossType, &b_muon_energyLossType);
   fChain->SetBranchAddress("muon_MeasEnergyLoss", &muon_MeasEnergyLoss, &b_muon_MeasEnergyLoss);
   fChain->SetBranchAddress("muon_MeasEnergyLossSigma", &muon_MeasEnergyLossSigma, &b_muon_MeasEnergyLossSigma);
   fChain->SetBranchAddress("muon_ParamEnergyLoss", &muon_ParamEnergyLoss, &b_muon_ParamEnergyLoss);
   fChain->SetBranchAddress("muon_ParamEnergyLossSigmaMinus", &muon_ParamEnergyLossSigmaMinus, &b_muon_ParamEnergyLossSigmaMinus);
   fChain->SetBranchAddress("muon_ParamEnergyLossSigmaPlus", &muon_ParamEnergyLossSigmaPlus, &b_muon_ParamEnergyLossSigmaPlus);
   fChain->SetBranchAddress("metFinalClus", &metFinalClus, &b_metFinalClus);
   fChain->SetBranchAddress("metFinalClusPx", &metFinalClusPx, &b_metFinalClusPx);
   fChain->SetBranchAddress("metFinalClusPy", &metFinalClusPy, &b_metFinalClusPy);
   fChain->SetBranchAddress("metFinalClusSumEt", &metFinalClusSumEt, &b_metFinalClusSumEt);
   fChain->SetBranchAddress("metFinalClusPhi", &metFinalClusPhi, &b_metFinalClusPhi);
   fChain->SetBranchAddress("metFinalTrk", &metFinalTrk, &b_metFinalTrk);
   fChain->SetBranchAddress("metFinalTrkPx", &metFinalTrkPx, &b_metFinalTrkPx);
   fChain->SetBranchAddress("metFinalTrkPy", &metFinalTrkPy, &b_metFinalTrkPy);
   fChain->SetBranchAddress("metFinalTrkSumEt", &metFinalTrkSumEt, &b_metFinalTrkSumEt);
   fChain->SetBranchAddress("metFinalTrkPhi", &metFinalTrkPhi, &b_metFinalTrkPhi);
   fChain->SetBranchAddress("ntruths", &ntruths, &b_ntruths);
   fChain->SetBranchAddress("truth_E", &truth_E, &b_truth_E);
   fChain->SetBranchAddress("truth_pt", &truth_pt, &b_truth_pt);
   fChain->SetBranchAddress("truth_phi", &truth_phi, &b_truth_phi);
   fChain->SetBranchAddress("truth_eta", &truth_eta, &b_truth_eta);
   fChain->SetBranchAddress("truth_pdgId", &truth_pdgId, &b_truth_pdgId);
   fChain->SetBranchAddress("truth_status", &truth_status, &b_truth_status);
   fChain->SetBranchAddress("truth_barcode", &truth_barcode, &b_truth_barcode);
   fChain->SetBranchAddress("truth_is_higgs", &truth_is_higgs, &b_truth_is_higgs);
   fChain->SetBranchAddress("truth_is_bhad", &truth_is_bhad, &b_truth_is_bhad);
   fChain->SetBranchAddress("truth_Bdecay_x", &truth_Bdecay_x, &b_truth_Bdecay_x);
   fChain->SetBranchAddress("truth_Bdecay_y", &truth_Bdecay_y, &b_truth_Bdecay_y);
   fChain->SetBranchAddress("truth_Bdecay_z", &truth_Bdecay_z, &b_truth_Bdecay_z);
   fChain->SetBranchAddress("truth_nParents", &truth_nParents, &b_truth_nParents);
   fChain->SetBranchAddress("truth_parent_pdgId", &truth_parent_pdgId, &b_truth_parent_pdgId);
   fChain->SetBranchAddress("truth_parent_barcode", &truth_parent_barcode, &b_truth_parent_barcode);
   fChain->SetBranchAddress("truth_parent_status", &truth_parent_status, &b_truth_parent_status);
   fChain->SetBranchAddress("truth_nChildren", &truth_nChildren, &b_truth_nChildren);
   fChain->SetBranchAddress("truth_child_pdgId", &truth_child_pdgId, &b_truth_child_pdgId);
   fChain->SetBranchAddress("truth_child_barcode", &truth_child_barcode, &b_truth_child_barcode);
   fChain->SetBranchAddress("truth_child_status", &truth_child_status, &b_truth_child_status);
   fChain->SetBranchAddress("truth_mtt", &truth_mtt, &b_truth_mtt);
   fChain->SetBranchAddress("EventPass_XhhL1", &EventPass_XhhL1, &b_EventPass_XhhL1);
   fChain->SetBranchAddress("EventPass_XhhHLT", &EventPass_XhhHLT, &b_EventPass_XhhHLT);
   fChain->SetBranchAddress("EventPass_XhhTrig", &EventPass_XhhTrig, &b_EventPass_XhhTrig);
   fChain->SetBranchAddress("hcand_resolved_n", &hcand_resolved_n, &b_hcand_resolved_n);
   fChain->SetBranchAddress("hcand_resolved_pt", &hcand_resolved_pt, &b_hcand_resolved_pt);
   fChain->SetBranchAddress("hcand_resolved_eta", &hcand_resolved_eta, &b_hcand_resolved_eta);
   fChain->SetBranchAddress("hcand_resolved_phi", &hcand_resolved_phi, &b_hcand_resolved_phi);
   fChain->SetBranchAddress("hcand_resolved_m", &hcand_resolved_m, &b_hcand_resolved_m);
   fChain->SetBranchAddress("hcand_resolved_dRjj", &hcand_resolved_dRjj, &b_hcand_resolved_dRjj);
   fChain->SetBranchAddress("jet_ak4emtopo_asso_idx_in_resolvedJets", &jet_ak4emtopo_asso_idx_in_resolvedJets, &b_jet_ak4emtopo_asso_idx_in_resolvedJets);
   fChain->SetBranchAddress("lepTop_pt", &lepTop_pt, &b_lepTop_pt);
   fChain->SetBranchAddress("lepTop_eta", &lepTop_eta, &b_lepTop_eta);
   fChain->SetBranchAddress("lepTop_phi", &lepTop_phi, &b_lepTop_phi);
   fChain->SetBranchAddress("lepTop_m", &lepTop_m, &b_lepTop_m);
   fChain->SetBranchAddress("lepTop_dRmj", &lepTop_dRmj, &b_lepTop_dRmj);
   fChain->SetBranchAddress("leptop_jet_idx_in_lepTopJets", &leptop_jet_idx_in_lepTopJets, &b_leptop_jet_idx_in_lepTopJets);
   fChain->SetBranchAddress("leptop_muon_pt", &leptop_muon_pt, &b_leptop_muon_pt);
   fChain->SetBranchAddress("leptop_muon_eta", &leptop_muon_eta, &b_leptop_muon_eta);
   fChain->SetBranchAddress("leptop_muon_phi", &leptop_muon_phi, &b_leptop_muon_phi);
   fChain->SetBranchAddress("leptop_muon_m", &leptop_muon_m, &b_leptop_muon_m);
   fChain->SetBranchAddress("leptop_muon_ptcone20", &leptop_muon_ptcone20, &b_leptop_muon_ptcone20);
   fChain->SetBranchAddress("leptop_met", &leptop_met, &b_leptop_met);
   fChain->SetBranchAddress("leptop_metphi", &leptop_metphi, &b_leptop_metphi);
   fChain->SetBranchAddress("leptop_dPhimmet", &leptop_dPhimmet, &b_leptop_dPhimmet);
   fChain->SetBranchAddress("leptop_Mt", &leptop_Mt, &b_leptop_Mt);
   fChain->SetBranchAddress("hcand_boosted_n", &hcand_boosted_n, &b_hcand_boosted_n);
   fChain->SetBranchAddress("hcand_boosted_pt", &hcand_boosted_pt, &b_hcand_boosted_pt);
   fChain->SetBranchAddress("hcand_boosted_eta", &hcand_boosted_eta, &b_hcand_boosted_eta);
   fChain->SetBranchAddress("hcand_boosted_phi", &hcand_boosted_phi, &b_hcand_boosted_phi);
   fChain->SetBranchAddress("hcand_boosted_m", &hcand_boosted_m, &b_hcand_boosted_m);
   fChain->SetBranchAddress("hcand_boosted_htag_loose", &hcand_boosted_htag_loose, &b_hcand_boosted_htag_loose);
   fChain->SetBranchAddress("hcand_boosted_htag_medium", &hcand_boosted_htag_medium, &b_hcand_boosted_htag_medium);
   fChain->SetBranchAddress("hcand_boosted_htag_tight", &hcand_boosted_htag_tight, &b_hcand_boosted_htag_tight);
   fChain->SetBranchAddress("hcand_boosted_Wtag_medium", &hcand_boosted_Wtag_medium, &b_hcand_boosted_Wtag_medium);
   fChain->SetBranchAddress("hcand_boosted_Ztag_medium", &hcand_boosted_Ztag_medium, &b_hcand_boosted_Ztag_medium);
   fChain->SetBranchAddress("hcand_boosted_Wtag_tight", &hcand_boosted_Wtag_tight, &b_hcand_boosted_Wtag_tight);
   fChain->SetBranchAddress("hcand_boosted_Ztag_tight", &hcand_boosted_Ztag_tight, &b_hcand_boosted_Ztag_tight);
   fChain->SetBranchAddress("hcand_boosted_dRjj", &hcand_boosted_dRjj, &b_hcand_boosted_dRjj);
   fChain->SetBranchAddress("hcand_boosted_D2", &hcand_boosted_D2, &b_hcand_boosted_D2);
   fChain->SetBranchAddress("hcand_boosted_Tau21", &hcand_boosted_Tau21, &b_hcand_boosted_Tau21);
   fChain->SetBranchAddress("hcand_boosted_Tau21WTA", &hcand_boosted_Tau21WTA, &b_hcand_boosted_Tau21WTA);
   fChain->SetBranchAddress("hcand_boosted_nTrack", &hcand_boosted_nTrack, &b_hcand_boosted_nTrack);
   fChain->SetBranchAddress("hcand_boosted_nHBosons", &hcand_boosted_nHBosons, &b_hcand_boosted_nHBosons);
   fChain->SetBranchAddress("hcand_boosted_nWBosons", &hcand_boosted_nWBosons, &b_hcand_boosted_nWBosons);
   fChain->SetBranchAddress("hcand_boosted_nZBosons", &hcand_boosted_nZBosons, &b_hcand_boosted_nZBosons);
   fChain->SetBranchAddress("jet_ak2track_asso_n", &jet_ak2track_asso_n, &b_jet_ak2track_asso_n);
   fChain->SetBranchAddress("jet_ak2track_asso_n_addl", &jet_ak2track_asso_n_addl, &b_jet_ak2track_asso_n_addl);
   fChain->SetBranchAddress("jet_ak2track_asso_pt", &jet_ak2track_asso_pt, &b_jet_ak2track_asso_pt);
   fChain->SetBranchAddress("jet_ak2track_asso_eta", &jet_ak2track_asso_eta, &b_jet_ak2track_asso_eta);
   fChain->SetBranchAddress("jet_ak2track_asso_phi", &jet_ak2track_asso_phi, &b_jet_ak2track_asso_phi);
   fChain->SetBranchAddress("jet_ak2track_asso_m", &jet_ak2track_asso_m, &b_jet_ak2track_asso_m);
   fChain->SetBranchAddress("jet_ak2track_asso_MV2c00", &jet_ak2track_asso_MV2c00, &b_jet_ak2track_asso_MV2c00);
   fChain->SetBranchAddress("jet_ak2track_asso_MV2c10", &jet_ak2track_asso_MV2c10, &b_jet_ak2track_asso_MV2c10);
   fChain->SetBranchAddress("jet_ak2track_asso_MV2c20", &jet_ak2track_asso_MV2c20, &b_jet_ak2track_asso_MV2c20);
   fChain->SetBranchAddress("jet_ak2track_asso_MV2c100", &jet_ak2track_asso_MV2c100, &b_jet_ak2track_asso_MV2c100);
   fChain->SetBranchAddress("jet_ak2track_asso_sys", &jet_ak2track_asso_sys, &b_jet_ak2track_asso_sys);
   fChain->SetBranchAddress("jet_ak2track_asso_sysname", &jet_ak2track_asso_sysname, &b_jet_ak2track_asso_sysname);
   fChain->SetBranchAddress("boosted_bevent_sys", &boosted_bevent_sys, &b_boosted_bevent_sys);
   fChain->SetBranchAddress("truth_hcand_boosted_n", &truth_hcand_boosted_n, &b_truth_hcand_boosted_n);
   fChain->SetBranchAddress("truth_hcand_boosted_match", &truth_hcand_boosted_match, &b_truth_hcand_boosted_match);
   fChain->SetBranchAddress("truth_hcand_boosted_pt", &truth_hcand_boosted_pt, &b_truth_hcand_boosted_pt);
   fChain->SetBranchAddress("truth_hcand_boosted_eta", &truth_hcand_boosted_eta, &b_truth_hcand_boosted_eta);
   fChain->SetBranchAddress("truth_hcand_boosted_phi", &truth_hcand_boosted_phi, &b_truth_hcand_boosted_phi);
   fChain->SetBranchAddress("truth_hcand_boosted_m", &truth_hcand_boosted_m, &b_truth_hcand_boosted_m);
   fChain->SetBranchAddress("weight", &weight, &b_weight);
   fChain->SetBranchAddress("weight_xs", &weight_xs, &b_weight_xs);
   Notify();
}

Bool_t MiniTree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void MiniTree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t MiniTree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef MiniTree_cxx
