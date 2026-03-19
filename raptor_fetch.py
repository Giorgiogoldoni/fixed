#!/usr/bin/env python3
"""
RAPTOR Fetch — GitHub Actions
Scarica dati Yahoo Finance per tutti i 699 ticker,
calcola tutti gli indicatori e salva raptor_data.json
"""

import json, time, datetime
import yfinance as yf

# ═══════════════════════════════════════════════════════
#  TICKER LIST (699 ticker)
# ═══════════════════════════════════════════════════════
TICKERS = [{"y":"IAEX.AS","c":"Paesi","t":"IAEX"},{"y":"TOF.AS","c":"ATTIVO","t":"TOF"},{"y":"18MN.DE","c":"Lazy","t":"18MN"},{"y":"7USH.DE","c":"BOND","t":"7USH"},{"y":"CBUH.DE","c":"ATTIVO","t":"CBUH"},{"y":"CEB1.DE","c":"BOND","t":"CEB1"},{"y":"CEB4.DE","c":"NEW AREA","t":"CEB4"},{"y":"GXDW","c":"Paesi","t":"GXDW"},{"y":"DBZB.DE","c":"Lazy","t":"DBZB"},{"y":"EUNY.DE","c":"ATTIVO","t":"EUNY"},{"y":"FTGM.DE","c":"ATTIVO","t":"FTGM"},{"y":"IBC5.DE","c":"BOND","t":"IBC5"},{"y":"IBCJ.DE","c":"Paesi","t":"IBCJ"},{"y":"IQQ9.DE","c":"NEW AREA","t":"IQQ9"},{"y":"IQQF.DE","c":"NEW AREA","t":"IQQF"},{"y":"IS04.DE","c":"BOND","t":"IS04"},{"y":"IS3C.DE","c":"Lazy","t":"IS3C"},{"y":"IS3N.DE","c":"Lazy","t":"IS3N"},{"y":"IS3U.DE","c":"Paesi","t":"IS3U"},{"y":"ISPA.DE","c":"ATTIVO","t":"ISPA"},{"y":"IUSQ.DE","c":"Lazy","t":"IUSQ"},{"y":"IUSS.DE","c":"Paesi","t":"IUSS"},{"y":"LCUJ.DE","c":"Lazy","t":"LCUJ"},{"y":"MJMT.DE","c":"ATTIVO","t":"MJMT"},{"y":"QDVA.DE","c":"ATTIVO","t":"QDVA"},{"y":"SPP5.DE","c":"BOND","t":"SPP5"},{"y":"SPYX.DE","c":"ATTIVO","t":"SPYX"},{"y":"SXR1.DE","c":"Lazy","t":"SXR1"},{"y":"SXRT.DE","c":"Lazy","t":"SXRT"},{"y":"SXRU.DE","c":"NEW AREA","t":"SXRU"},{"y":"SXRW.DE","c":"Lazy","t":"SXRW"},{"y":"VGWE.DE","c":"ATTIVO","t":"VGWE"},{"y":"VUKG.DE","c":"Paesi","t":"VUKG"},{"y":"XBAS.DE","c":"Paesi","t":"XBAS"},{"y":"XCS3.DE","c":"Paesi","t":"XCS3"},{"y":"XCS4.DE","c":"Paesi","t":"XCS4"},{"y":"XD9E.DE","c":"Lazy","t":"XD9E"},{"y":"XD9U.DE","c":"Lazy","t":"XD9U"},{"y":"XDEM.DE","c":"ATTIVO","t":"XDEM"},{"y":"XESD.DE","c":"Paesi","t":"XESD"},{"y":"XGIN.DE","c":"Lazy","t":"XGIN"},{"y":"XMKA.DE","c":"Paesi","t":"XMKA"},{"y":"XPQP.DE","c":"Paesi","t":"XPQP"},{"y":"XWEM.DE","c":"ATTIVO","t":"XWEM"},{"y":"F701.F","c":"ATTIVO","t":"F701"},{"y":"F702.F","c":"ATTIVO","t":"F702"},{"y":"F703.F","c":"ATTIVO","t":"F703"},{"y":"IUSN.F","c":"ADVICE","t":"IUSN"},{"y":"IVAI.MI","c":"Tematici","t":"IVAI"},{"y":"IVDF.DE","c":"Tematici","t":"IVDF"},{"y":"NQSE.F","c":"NEW AREA","t":"NQSE"},{"y":"NTSZ.DE","c":"ATTIVO","t":"NTSZ"},{"y":"IEFM.L","c":"ATTIVO","t":"IEFM"},{"y":"A01U.MI","c":"BOND","t":"A01U"},{"y":"ACT20.MI","c":"ATTIVO","t":"ACT20"},{"y":"ACT60.MI","c":"ATTIVO","t":"ACT60"},{"y":"ACTEQ.MI","c":"ATTIVO","t":"ACTEQ"},{"y":"ADLU.MI","c":"BOND","t":"ADLU"},{"y":"AEGE.MI","c":"BOND","t":"AEGE"},{"y":"AGEB.MI","c":"BOND","t":"AGEB"},{"y":"AGED.MI","c":"Tematici","t":"AGED"},{"y":"AGGH.MI","c":"BOND","t":"AGGH"},{"y":"AI4UJ.MI","c":"Tematici","t":"AI4UJ"},{"y":"AIAA.MI","c":"Tematici","t":"AIAA"},{"y":"AIAI.MI","c":"Tematici","t":"AIAI"},{"y":"AICU.MI","c":"BOND","t":"AICU"},{"y":"AIGA.MI","c":"Materie","t":"AIGA"},{"y":"AIGC.MI","c":"Materie","t":"AIGC"},{"y":"AIGE.MI","c":"Materie","t":"AIGE"},{"y":"AIGG.MI","c":"Materie","t":"AIGG"},{"y":"AIGI.MI","c":"Materie","t":"AIGI"},{"y":"AIGL.MI","c":"Materie","t":"AIGL"},{"y":"AIGO.MI","c":"Materie","t":"AIGO"},{"y":"AIGP.MI","c":"Materie","t":"AIGP"},{"y":"AIGS.MI","c":"Materie","t":"AIGS"},{"y":"AINF.MI","c":"Tematici","t":"AINF"},{"y":"AIQE.MI","c":"Tematici","t":"AIQE"},{"y":"ALAT.MI","c":"NEW AREA","t":"ALAT"},{"y":"ALUM.MI","c":"Materie","t":"ALUM"},{"y":"ANAU.MI","c":"ADVICE","t":"ANAU"},{"y":"AQWA.MI","c":"Tematici","t":"AQWA"},{"y":"ARMI.MI","c":"Tematici","t":"ARMI"},{"y":"ARMR.MI","c":"Tematici","t":"ARMR"},{"y":"ASRD.MI","c":"BOND","t":"ASRD"},{"y":"AT1.MI","c":"BOND","t":"AT1"},{"y":"AUCO.MI","c":"Tematici","t":"AUCO"},{"y":"AUHEUA.MI","c":"Paesi","t":"AUHEUA"},{"y":"BATT.MI","c":"Tematici","t":"BATT"},{"y":"BBTR.MI","c":"BOND","t":"BBTR"},{"y":"BCHN.MI","c":"Settoriali","t":"BCHN"},{"y":"BENE.MI","c":"Materie","t":"BENE"},{"y":"BIODV.MI","c":"Settoriali","t":"BIODV"},{"y":"BIOT.MI","c":"Tematici","t":"BIOT"},{"y":"BKCH.MI","c":"Tematici","t":"BKCH"},{"y":"BLTH.MI","c":"Tematici","t":"BLTH"},{"y":"BNK.MI","c":"Settoriali","t":"BNK"},{"y":"BNKE.MI","c":"Settoriali","t":"BNKE"},{"y":"BOTZ.MI","c":"Tematici","t":"BOTZ"},{"y":"BRENT.MI","c":"Materie","t":"BRENT"},{"y":"BRES.MI","c":"Settoriali","t":"BRES"},{"y":"BRIJ.MI","c":"Tematici","t":"BRIJ"},{"y":"BRND.MI","c":"Materie","t":"BRND"},{"y":"BRNT.MI","c":"Materie","t":"BRNT"},{"y":"BSRIC.MI","c":"BOND","t":"BSRIC"},{"y":"BT27.MI","c":"BOND","t":"BT27"},{"y":"BTC.MI","c":"Tematici","t":"BTC"},{"y":"BTECH.MI","c":"Tematici","t":"BTECH"},{"y":"BTECJ.MI","c":"Tematici","t":"BTECJ"},{"y":"BTP10.MI","c":"BOND","t":"BTP10"},{"y":"BUG.MI","c":"Tematici","t":"BUG"},{"y":"C40.MI","c":"Paesi","t":"C40"},{"y":"CAHEUA.MI","c":"NEW AREA","t":"CAHEUA"},{"y":"CARB.MI","c":"Materie","t":"CARB"},{"y":"CAUT.MI","c":"Tematici","t":"CAUT"},{"y":"CBSUSA.MI","c":"BOND","t":"CBSUSA"},{"y":"CCEUAS.MI","c":"Materie","t":"CCEUAS"},{"y":"CCUSAS.MI","c":"Materie","t":"CCUSAS"},{"y":"CHIP.MI","c":"ADVICE","t":"CHIP"},{"y":"CHM.MI","c":"Settoriali","t":"CHM"},{"y":"CIBR.MI","c":"ADVICE","t":"CIBR"},{"y":"CIT.MI","c":"Tematici","t":"CIT"},{"y":"CITE.MI","c":"Tematici","t":"CITE"},{"y":"CITY.MI","c":"Tematici","t":"CITY"},{"y":"CLIP.MI","c":"BOND","t":"CLIP"},{"y":"CLOU.MI","c":"Tematici","t":"CLOU"},{"y":"CMOC.MI","c":"Materie","t":"CMOC"},{"y":"CMOD.MI","c":"Materie","t":"CMOD"},{"y":"CMOE.MI","c":"Materie","t":"CMOE"},{"y":"CN1.MI","c":"Paesi","t":"CN1"},{"y":"CO2.MI","c":"Materie","t":"CO2"},{"y":"COCO.MI","c":"Materie","t":"COCO"},{"y":"COFF.MI","c":"Materie","t":"COFF"},{"y":"COMF.MI","c":"Materie","t":"COMF"},{"y":"COMH.MI","c":"Materie","t":"COMH"},{"y":"COMO.MI","c":"Materie","t":"COMO"},{"y":"COPA.MI","c":"Materie","t":"COPA"},{"y":"COPM.MI","c":"Tematici","t":"COPM"},{"y":"COPR.MI","c":"Tematici","t":"COPR"},{"y":"COPX.MI","c":"Tematici","t":"COPX"},{"y":"CORN.MI","c":"Materie","t":"CORN"},{"y":"COTN.MI","c":"Materie","t":"COTN"},{"y":"CROP.MI","c":"Tematici","t":"CROP"},{"y":"CRRY.MI","c":"Materie","t":"CRRY"},{"y":"CRUD.MI","c":"Materie","t":"CRUD"},{"y":"CSBGE7.MI","c":"BOND","t":"CSBGE7"},{"y":"CSBGU3.MI","c":"BOND","t":"CSBGU3"},{"y":"CSBGU7.MI","c":"BOND","t":"CSBGU7"},{"y":"CSCA.MI","c":"NEW AREA","t":"CSCA"},{"y":"CSEMAS.MI","c":"NEW AREA","t":"CSEMAS"},{"y":"CSMIB.MI","c":"Paesi","t":"CSMIB"},{"y":"CSNDX.MI","c":"Paesi","t":"CSNDX"},{"y":"CSPXJ.MI","c":"NEW AREA","t":"CSPXJ"},{"y":"CSSPX.MI","c":"ADVICE","t":"CSSPX"},{"y":"CSUS.MI","c":"ADVICE","t":"CSUS"},{"y":"CSUSS.MI","c":"ADVICE","t":"CSUSS"},{"y":"CTEK.MI","c":"Tematici","t":"CTEK"},{"y":"CURE.MI","c":"Tematici","t":"CURE"},{"y":"CWE.MI","c":"Settoriali","t":"CWE"},{"y":"CYBO.MI","c":"Tematici","t":"CYBO"},{"y":"CYBR.MI","c":"Settoriali","t":"CYBR"},{"y":"DAPP.MI","c":"Tematici","t":"DAPP"},{"y":"DEFS.MI","c":"Settoriali","t":"DEFS"},{"y":"DEMR.MI","c":"ATTIVO","t":"DEMR"},{"y":"DFND.MI","c":"Tematici","t":"DFND"},{"y":"DFNS.MI","c":"Tematici","t":"DFNS"},{"y":"DGTL.MI","c":"Tematici","t":"DGTL"},{"y":"DISW.MI","c":"Settoriali","t":"DISW"},{"y":"DJE.MI","c":"Paesi","t":"DJE"},{"y":"DMAT.MI","c":"Tematici","t":"DMAT"},{"y":"DOCT.MI","c":"Tematici","t":"DOCT"},{"y":"DPAY.MI","c":"Tematici","t":"DPAY"},{"y":"DRVE.MI","c":"Tematici","t":"DRVE"},{"y":"DXJF.MI","c":"ATTIVO","t":"DXJF"},{"y":"EALU.MI","c":"Materie","t":"EALU"},{"y":"EBIZ.MI","c":"Tematici","t":"EBIZ"},{"y":"EBRT.MI","c":"Materie","t":"EBRT"},{"y":"EBUY.MI","c":"Tematici","t":"EBUY"},{"y":"ECAR.MI","c":"Tematici","t":"ECAR"},{"y":"ECEH.MI","c":"Materie","t":"ECEH"},{"y":"ECO.MI","c":"BOND","t":"ECO"},{"y":"ECOF.MI","c":"Materie","t":"ECOF"},{"y":"ECOM.MI","c":"Tematici","t":"ECOM"},{"y":"ECOP.MI","c":"Materie","t":"ECOP"},{"y":"ECR1.MI","c":"BOND","t":"ECR1"},{"y":"ECRD.MI","c":"Materie","t":"ECRD"},{"y":"ECRN.MI","c":"Materie","t":"ECRN"},{"y":"ECRP3.MI","c":"BOND","t":"ECRP3"},{"y":"ECTN.MI","c":"Materie","t":"ECTN"},{"y":"EDOC.MI","c":"Tematici","t":"EDOC"},{"y":"EEA.MI","c":"Tematici","t":"EEA"},{"y":"EEIA.MI","c":"ATTIVO","t":"EEIA"},{"y":"EENG.MI","c":"Settoriali","t":"EENG"},{"y":"EFCM.MI","c":"Materie","t":"EFCM"},{"y":"EGEHE.MI","c":"Settoriali","t":"EGEHE"},{"y":"EGOV.MI","c":"BOND","t":"EGOV"},{"y":"EHYA.MI","c":"BOND","t":"EHYA"},{"y":"EIMI.MI","c":"ADVICE","t":"EIMI"},{"y":"EIMT.MI","c":"Materie","t":"EIMT"},{"y":"ELCR.MI","c":"Tematici","t":"ELCR"},{"y":"EM1015.MI","c":"BOND","t":"EM1015"},{"y":"EM35.MI","c":"BOND","t":"EM35"},{"y":"EM710.MI","c":"BOND","t":"EM710"},{"y":"EMGH.MI","c":"BOND","t":"EMGH"},{"y":"EMI.MI","c":"BOND","t":"EMI"},{"y":"EMOVE.MI","c":"Tematici","t":"EMOVE"},{"y":"EMOVJ.MI","c":"Tematici","t":"EMOVJ"},{"y":"EMQQ.MI","c":"Settoriali","t":"EMQQ"},{"y":"ENCO.MI","c":"Materie","t":"ENCO"},{"y":"ENERW.MI","c":"Settoriali","t":"ENERW"},{"y":"ENGS.MI","c":"Materie","t":"ENGS"},{"y":"ENIK.MI","c":"Materie","t":"ENIK"},{"y":"ENRG.MI","c":"Settoriali","t":"ENRG"},{"y":"ENTR.MI","c":"Materie","t":"ENTR"},{"y":"EPRA.MI","c":"Tematici","t":"EPRA"},{"y":"EPRE.MI","c":"Tematici","t":"EPRE"},{"y":"EROX.MI","c":"ADVICE","t":"EROX"},{"y":"ESGO.MI","c":"Tematici","t":"ESGO"},{"y":"ESOY.MI","c":"Materie","t":"ESOY"},{"y":"ESPO.MI","c":"Tematici","t":"ESPO"},{"y":"ESPY.MI","c":"Tematici","t":"ESPY"},{"y":"EST.MI","c":"NEW AREA","t":"EST"},{"y":"ESUG.MI","c":"Materie","t":"ESUG"},{"y":"ETFCRP.MI","c":"BOND","t":"ETFCRP"},{"y":"EUC.MI","c":"BOND","t":"EUC"},{"y":"EUES.MI","c":"BOND","t":"EUES"},{"y":"EWAT.MI","c":"Materie","t":"EWAT"},{"y":"EXS1.MI","c":"Paesi","t":"EXS1"},{"y":"EXXY.MI","c":"Materie","t":"EXXY"},{"y":"EZNC.MI","c":"Materie","t":"EZNC"},{"y":"FAMAMW.MI","c":"Tematici","t":"FAMAMW"},{"y":"FAMMAI.MI","c":"Tematici","t":"FAMMAI"},{"y":"FAMMWF.MI","c":"Tematici","t":"FAMMWF"},{"y":"FAMMWS.MI","c":"Tematici","t":"FAMMWS"},{"y":"FAMTEL.MI","c":"Tematici","t":"FAMTEL"},{"y":"FAMWCS.MI","c":"Tematici","t":"FAMWCS"},{"y":"FCRU.MI","c":"Materie","t":"FCRU"},{"y":"FGEA.MI","c":"ATTIVO","t":"FGEA"},{"y":"FINSW.MI","c":"Settoriali","t":"FINSW"},{"y":"FINX.MI","c":"Tematici","t":"FINX"},{"y":"FLUSA.MI","c":"BOND","t":"FLUSA"},{"y":"FLXI.MI","c":"Paesi","t":"FLXI"},{"y":"FLXT.MI","c":"Paesi","t":"FLXT"},{"y":"FLXU.MI","c":"Paesi","t":"FLXU"},{"y":"FMI.MI","c":"Paesi","t":"FMI"},{"y":"FOFD.MI","c":"Tematici","t":"FOFD"},{"y":"FOO.MI","c":"Settoriali","t":"FOO"},{"y":"FOOD.MI","c":"Settoriali","t":"FOOD"},{"y":"FUSU.MI","c":"ATTIVO","t":"FUSU"},{"y":"GAGG.MI","c":"BOND","t":"GAGG"},{"y":"GAGH.MI","c":"BOND","t":"GAGH"},{"y":"GAS.MI","c":"Materie","t":"GAS"},{"y":"GASRI.MI","c":"BOND","t":"GASRI"},{"y":"GCLE.MI","c":"Tematici","t":"GCLE"},{"y":"GCVE.MI","c":"BOND","t":"GCVE"},{"y":"GDIG.MI","c":"Tematici","t":"GDIG"},{"y":"GDX.MI","c":"Tematici","t":"GDX"},{"y":"GDXJ.MI","c":"Tematici","t":"GDXJ"},{"y":"GENDEE.MI","c":"Tematici","t":"GENDEE"},{"y":"GLUG.MI","c":"Tematici","t":"GLUG"},{"y":"GLUX.MI","c":"Tematici","t":"GLUX"},{"y":"GNOM.MI","c":"Tematici","t":"GNOM"},{"y":"GOAI.MI","c":"Tematici","t":"GOAI"},{"y":"GOVA.MI","c":"BOND","t":"GOVA"},{"y":"GRC.MI","c":"Paesi","t":"GRC"},{"y":"GRCTB.MI","c":"Settoriali","t":"GRCTB"},{"y":"GREAL.MI","c":"Settoriali","t":"GREAL"},{"y":"GSCE.MI","c":"Materie","t":"GSCE"},{"y":"GSM.MI","c":"Tematici","t":"GSM"},{"y":"HDRO.MI","c":"Tematici","t":"HDRO"},{"y":"HEAL.MI","c":"Tematici","t":"HEAL"},{"y":"HECB.MI","c":"BOND","t":"HECB"},{"y":"HERU.MI","c":"Tematici","t":"HERU"},{"y":"HGAE.MI","c":"BOND","t":"HGAE"},{"y":"HIDIJ.MI","c":"ATTIVO","t":"HIDIJ"},{"y":"HLT.MI","c":"Settoriali","t":"HLT"},{"y":"HLTW.MI","c":"Settoriali","t":"HLTW"},{"y":"HMXJ.MI","c":"ADVICE","t":"HMXJ"},{"y":"HNSC.MI","c":"Tematici","t":"HNSC"},{"y":"HPNA.MI","c":"Settoriali","t":"HPNA"},{"y":"HSTE.MI","c":"Paesi","t":"HSTE"},{"y":"HTWO.MI","c":"Tematici","t":"HTWO"},{"y":"HUCB.MI","c":"BOND","t":"HUCB"},{"y":"HUST.MI","c":"BOND","t":"HUST"},{"y":"HYDE.MI","c":"Tematici","t":"HYDE"},{"y":"HYGN.MI","c":"Tematici","t":"HYGN"},{"y":"HYLD.MI","c":"ADVICE","t":"HYLD"},{"y":"IAPD.MI","c":"NEW AREA","t":"IAPD"},{"y":"IBZL.MI","c":"Paesi","t":"IBZL"},{"y":"ICBR.MI","c":"Tematici","t":"ICBR"},{"y":"IEAA.MI","c":"BOND","t":"IEAA"},{"y":"IEGS.MI","c":"BOND","t":"IEGS"},{"y":"IEMB.MI","c":"ADVICE","t":"IEMB"},{"y":"IEMO.MI","c":"ATTIVO","t":"IEMO"},{"y":"IJPE.MI","c":"NEW AREA","t":"IJPE"},{"y":"IMIB.MI","c":"Paesi","t":"IMIB"},{"y":"INDG.MI","c":"Settoriali","t":"INDG"},{"y":"INDGW.MI","c":"Settoriali","t":"INDGW"},{"y":"INDI.MI","c":"Paesi","t":"INDI"},{"y":"INDO.MI","c":"Paesi","t":"INDO"},{"y":"INF1A.MI","c":"BOND","t":"INF1A"},{"y":"INFU.MI","c":"BOND","t":"INFU"},{"y":"INQQ.MI","c":"Tematici","t":"INQQ"},{"y":"INS.MI","c":"Settoriali","t":"INS"},{"y":"ISAC.MI","c":"NEW AREA","t":"ISAC"},{"y":"ISAG.MI","c":"Tematici","t":"ISAG"},{"y":"ISPY.MI","c":"Tematici","t":"ISPY"},{"y":"ITBL.MI","c":"Paesi","t":"ITBL"},{"y":"IU0E.MI","c":"BOND","t":"IU0E"},{"y":"IUSE.MI","c":"NEW AREA","t":"IUSE"},{"y":"IWDE.MI","c":"NEW AREA","t":"IWDE"},{"y":"IWMO.MI","c":"ATTIVO","t":"IWMO"},{"y":"IWVL.MI","c":"ADVICE","t":"IWVL"},{"y":"JEDI.MI","c":"Tematici","t":"JEDI"},{"y":"JRGE.MI","c":"NEW AREA","t":"JRGE"},{"y":"JU13.MI","c":"BOND","t":"JU13"},{"y":"KARS.MI","c":"Settoriali","t":"KARS"},{"y":"KOR.MI","c":"Paesi","t":"KOR"},{"y":"KRBN.MI","c":"Materie","t":"KRBN"},{"y":"KWBE.MI","c":"Tematici","t":"KWBE"},{"y":"LABL.MI","c":"Tematici","t":"LABL"},{"y":"LAFRI.MI","c":"NEW AREA","t":"LAFRI"},{"y":"LCCN.MI","c":"Paesi","t":"LCCN"},{"y":"LEAD.MI","c":"Materie","t":"LEAD"},{"y":"LGUS.MI","c":"Paesi","t":"LGUS"},{"y":"LINXB.MI","c":"ATTIVO","t":"LINXB"},{"y":"LITM.MI","c":"Tematici","t":"LITM"},{"y":"LITU.MI","c":"Tematici","t":"LITU"},{"y":"LOCK.MI","c":"Tematici","t":"LOCK"},{"y":"LTAM.MI","c":"NEW AREA","t":"LTAM"},{"y":"LVO.MI","c":"Materie","t":"LVO"},{"y":"MACV.MI","c":"ATTIVO","t":"MACV"},{"y":"MAGR.MI","c":"ATTIVO","t":"MAGR"},{"y":"MATW.MI","c":"Settoriali","t":"MATW"},{"y":"MCHN.MI","c":"Paesi","t":"MCHN"},{"y":"MCHT.MI","c":"Tematici","t":"MCHT"},{"y":"META.MI","c":"Materie","t":"META"},{"y":"METAA.MI","c":"Tematici","t":"METAA"},{"y":"METAJ.MI","c":"Tematici","t":"METAJ"},{"y":"METE.MI","c":"Tematici","t":"METE"},{"y":"METL.MI","c":"Tematici","t":"METL"},{"y":"MILL.MI","c":"Tematici","t":"MILL"},{"y":"MLPS.MI","c":"Tematici","t":"MLPS"},{"y":"MODR.MI","c":"ATTIVO","t":"MODR"},{"y":"MTAV.MI","c":"Tematici","t":"MTAV"},{"y":"MTVS.MI","c":"Tematici","t":"MTVS"},{"y":"NATO.MI","c":"Settoriali","t":"NATO"},{"y":"NCLR.MI","c":"Tematici","t":"NCLR"},{"y":"NGAS.MI","c":"Materie","t":"NGAS"},{"y":"NICK.MI","c":"Materie","t":"NICK"},{"y":"NRJC.MI","c":"Tematici","t":"NRJC"},{"y":"NTSG.MI","c":"ATTIVO","t":"NTSG"},{"y":"NUCL.MI","c":"Tematici","t":"NUCL"},{"y":"OCEAN.MI","c":"Settoriali","t":"OCEAN"},{"y":"OIH.MI","c":"Tematici","t":"OIH"},{"y":"OVER.MI","c":"BOND","t":"OVER"},{"y":"PAVE.MI","c":"Tematici","t":"PAVE"},{"y":"PCOM.MI","c":"Materie","t":"PCOM"},{"y":"PHAG.MI","c":"Materie","t":"PHAG"},{"y":"PHPD.MI","c":"Materie","t":"PHPD"},{"y":"PHPM.MI","c":"Materie","t":"PHPM"},{"y":"PHPT.MI","c":"Materie","t":"PHPT"},{"y":"PJSR.MI","c":"BOND","t":"PJSR"},{"y":"QNTM.MI","c":"Tematici","t":"QNTM"},{"y":"QTOP.MI","c":"Paesi","t":"QTOP"},{"y":"QUAD.MI","c":"Tematici","t":"QUAD"},{"y":"RARE.MI","c":"Tematici","t":"RARE"},{"y":"RAYZ.MI","c":"Tematici","t":"RAYZ"},{"y":"RBOT.MI","c":"ADVICE","t":"RBOT"},{"y":"REMX.MI","c":"Tematici","t":"REMX"},{"y":"RENW.MI","c":"Tematici","t":"RENW"},{"y":"REUS.MI","c":"Tematici","t":"REUS"},{"y":"REUSE.MI","c":"Settoriali","t":"REUSE"},{"y":"RNRG.MI","c":"Tematici","t":"RNRG"},{"y":"ROBO.MI","c":"Tematici","t":"ROBO"},{"y":"ROE.MI","c":"Tematici","t":"ROE"},{"y":"SAUDI.MI","c":"Paesi","t":"SAUDI"},{"y":"SAUS.MI","c":"Paesi","t":"SAUS"},{"y":"SBIO.MI","c":"Settoriali","t":"SBIO"},{"y":"SCITY.MI","c":"Tematici","t":"SCITY"},{"y":"SDG9.MI","c":"Tematici","t":"SDG9"},{"y":"SEMA.MI","c":"NEW AREA","t":"SEMA"},{"y":"SEME.MI","c":"Tematici","t":"SEME"},{"y":"SGBS.MI","c":"Materie","t":"SGBS"},{"y":"SHEME.MI","c":"BOND","t":"SHEME"},{"y":"SILV.MI","c":"Tematici","t":"SILV"},{"y":"SJPA.MI","c":"NEW AREA","t":"SJPA"},{"y":"SMCX.MI","c":"ADVICE","t":"SMCX"},{"y":"SMEA.MI","c":"ADVICE","t":"SMEA"},{"y":"SMH.MI","c":"Tematici","t":"SMH"},{"y":"SNSR.MI","c":"Tematici","t":"SNSR"},{"y":"SOLR.MI","c":"Tematici","t":"SOLR"},{"y":"SOYB.MI","c":"Materie","t":"SOYB"},{"y":"SOYO.MI","c":"Materie","t":"SOYO"},{"y":"SP1E.MI","c":"Paesi","t":"SP1E"},{"y":"SP5A.MI","c":"ADVICE","t":"SP5A"},{"y":"SPXE.MI","c":"Paesi","t":"SPXE"},{"y":"SPXJ.MI","c":"Paesi","t":"SPXJ"},{"y":"SPY5.MI","c":"Paesi","t":"SPY5"},{"y":"SRIUC.MI","c":"BOND","t":"SRIUC"},{"y":"SRSA.MI","c":"Paesi","t":"SRSA"},{"y":"STAW.MI","c":"Settoriali","t":"STAW"},{"y":"DFSV.DE","c":"SPDR EURO","t":"DFSV"},{"y":"STKX.MI","c":"SPDR EURO","t":"STKX"},{"y":"STNX.MI","c":"SPDR EURO","t":"STNX"},{"y":"STPX.MI","c":"SPDR EURO","t":"STPX"},{"y":"STQX.MI","c":"SPDR EURO","t":"STQX"},{"y":"STRX.MI","c":"SPDR EURO","t":"STRX"},{"y":"STSX.MI","c":"SPDR EURO","t":"STSX"},{"y":"STTX.MI","c":"SPDR EURO","t":"STTX"},{"y":"STUX.MI","c":"SPDR EURO","t":"STUX"},{"y":"SUGA.MI","c":"Materie","t":"SUGA"},{"y":"SW2CHB.MI","c":"Paesi","t":"SW2CHB"},{"y":"SWDA.MI","c":"ADVICE","t":"SWDA"},{"y":"SXLB.MI","c":"SPDR USA","t":"SXLB"},{"y":"SXLC.MI","c":"SPDR USA","t":"SXLC"},{"y":"SXLF.MI","c":"SPDR USA","t":"SXLF"},{"y":"SXLI.MI","c":"SPDR USA","t":"SXLI"},{"y":"SXLK.MI","c":"SPDR USA","t":"SXLK"},{"y":"SXLP.MI","c":"SPDR USA","t":"SXLP"},{"y":"SXLU.MI","c":"SPDR USA","t":"SXLU"},{"y":"SXLV.MI","c":"SPDR USA","t":"SXLV"},{"y":"SXLY.MI","c":"SPDR USA","t":"SXLY"},{"y":"T10A.MI","c":"BOND","t":"T10A"},{"y":"TELE.MI","c":"Settoriali","t":"TELE"},{"y":"TELEW.MI","c":"Settoriali","t":"TELEW"},{"y":"TIP1A.MI","c":"BOND","t":"TIP1A"},{"y":"TLCO.MI","c":"Tematici","t":"TLCO"},{"y":"TNO.MI","c":"Settoriali","t":"TNO"},{"y":"TNOW.MI","c":"Settoriali","t":"TNOW"},{"y":"TRVL.MI","c":"Settoriali","t":"TRVL"},{"y":"TTFW.MI","c":"Materie","t":"TTFW"},{"y":"TUR.MI","c":"Paesi","t":"TUR"},{"y":"U3O8.MI","c":"Tematici","t":"U3O8"},{"y":"UCRP.MI","c":"BOND","t":"UCRP"},{"y":"UGAS.MI","c":"Materie","t":"UGAS"},{"y":"UKE.MI","c":"Paesi","t":"UKE"},{"y":"UNIC.MI","c":"Tematici","t":"UNIC"},{"y":"URNJ.MI","c":"Tematici","t":"URNJ"},{"y":"URNU.MI","c":"ADVICE","t":"URNU"},{"y":"US1.MI","c":"BOND","t":"US1"},{"y":"US10C.MI","c":"BOND","t":"US10C"},{"y":"US7.MI","c":"BOND","t":"US7"},{"y":"USCBC.MI","c":"BOND","t":"USCBC"},{"y":"USIC.MI","c":"BOND","t":"USIC"},{"y":"USIG.MI","c":"BOND","t":"USIG"},{"y":"USTEC.MI","c":"Tematici","t":"USTEC"},{"y":"UTI.MI","c":"Settoriali","t":"UTI"},{"y":"UTIW.MI","c":"Settoriali","t":"UTIW"},{"y":"VAGF.MI","c":"BOND","t":"VAGF"},{"y":"VCDE.MI","c":"BOND","t":"VCDE"},{"y":"VDCA.MI","c":"BOND","t":"VDCA"},{"y":"VDCE.MI","c":"BOND","t":"VDCE"},{"y":"VDEA.MI","c":"BOND","t":"VDEA"},{"y":"VDST.MI","c":"BOND","t":"VDST"},{"y":"VECA.MI","c":"BOND","t":"VECA"},{"y":"VEGI.MI","c":"Tematici","t":"VEGI"},{"y":"VGEA.MI","c":"BOND","t":"VGEA"},{"y":"VITA.MI","c":"Settoriali","t":"VITA"},{"y":"VITU.MI","c":"Settoriali","t":"VITU"},{"y":"VJPE.MI","c":"Paesi","t":"VJPE"},{"y":"VNGA20.MI","c":"ATTIVO","t":"VNGA20"},{"y":"VNGA40.MI","c":"ATTIVO","t":"VNGA40"},{"y":"VNGA60.MI","c":"ATTIVO","t":"VNGA60"},{"y":"VNGA80.MI","c":"ATTIVO","t":"VNGA80"},{"y":"VOLT.MI","c":"Tematici","t":"VOLT"},{"y":"VPN.MI","c":"Tematici","t":"VPN"},{"y":"VSCF.MI","c":"BOND","t":"VSCF"},{"y":"VSGF.MI","c":"BOND","t":"VSGF"},{"y":"VUCE.MI","c":"BOND","t":"VUCE"},{"y":"VUKE.MI","c":"Paesi","t":"VUKE"},{"y":"VUSA.MI","c":"Paesi","t":"VUSA"},{"y":"WATC.MI","c":"Tematici","t":"WATC"},{"y":"WATT.MI","c":"Materie","t":"WATT"},{"y":"WBLK.MI","c":"Tematici","t":"WBLK"},{"y":"WCBR.MI","c":"Tematici","t":"WCBR"},{"y":"WCCA.MI","c":"Materie","t":"WCCA"},{"y":"WCLD.MI","c":"Settoriali","t":"WCLD"},{"y":"WCOA.MI","c":"Materie","t":"WCOA"},{"y":"WCOD.MI","c":"SPDR WORLD","t":"WCOD"},{"y":"WCOE.MI","c":"Materie","t":"WCOE"},{"y":"WCOS.MI","c":"SPDR WORLD","t":"WCOS"},{"y":"WDEF.MI","c":"Tematici","t":"WDEF"},{"y":"WDNA.MI","c":"Tematici","t":"WDNA"},{"y":"WEAT.MI","c":"Materie","t":"WEAT"},{"y":"WEB3.MI","c":"Tematici","t":"WEB3"},{"y":"WENT.MI","c":"Materie","t":"WENT"},{"y":"WENU.MI","c":"Materie","t":"WENU"},{"y":"WFIN.MI","c":"SPDR WORLD","t":"WFIN"},{"y":"WGRO.MI","c":"Tematici","t":"WGRO"},{"y":"WHEA.MI","c":"SPDR WORLD","t":"WHEA"},{"y":"WIND.MI","c":"SPDR WORLD","t":"WIND"},{"y":"WMAT.MI","c":"SPDR WORLD","t":"WMAT"},{"y":"WMGT.MI","c":"Tematici","t":"WMGT"},{"y":"WMIB.MI","c":"Paesi","t":"WMIB"},{"y":"WNAS.MI","c":"Paesi","t":"WNAS"},{"y":"WNDE.MI","c":"Tematici","t":"WNDE"},{"y":"WNDY.MI","c":"Tematici","t":"WNDY"},{"y":"WNRG.MI","c":"SPDR WORLD","t":"WNRG"},{"y":"WRNW.MI","c":"Tematici","t":"WRNW"},{"y":"WRTY.MI","c":"Paesi","t":"WRTY"},{"y":"WS5X.MI","c":"Paesi","t":"WS5X"},{"y":"WSLV.MI","c":"Tematici","t":"WSLV"},{"y":"WSPE.MI","c":"Paesi","t":"WSPE"},{"y":"WSPX.MI","c":"Paesi","t":"WSPX"},{"y":"WTAI.MI","c":"Tematici","t":"WTAI"},{"y":"WTEC.MI","c":"SPDR WORLD","t":"WTEC"},{"y":"WTEL.MI","c":"SPDR WORLD","t":"WTEL"},{"y":"WTI.MI","c":"Materie","t":"WTI"},{"y":"WTID.MI","c":"Materie","t":"WTID"},{"y":"WTRE.MI","c":"Tematici","t":"WTRE"},{"y":"WUTI.MI","c":"SPDR WORLD","t":"WUTI"},{"y":"X25E.MI","c":"BOND","t":"X25E"},{"y":"X7PS.MI","c":"Settoriali","t":"X7PS"},{"y":"XAGZ.MI","c":"Materie","t":"XAGZ"},{"y":"XAIX.MI","c":"ADVICE","t":"XAIX"},{"y":"XBAE.MI","c":"BOND","t":"XBAE"},{"y":"XBAG.MI","c":"BOND","t":"XBAG"},{"y":"XBLC.MI","c":"BOND","t":"XBLC"},{"y":"XBNK.MI","c":"BOND","t":"XBNK"},{"y":"XCHA.MI","c":"Paesi","t":"XCHA"},{"y":"XCS5.MI","c":"Paesi","t":"XCS5"},{"y":"XCTE.MI","c":"Tematici","t":"XCTE"},{"y":"XDAX.MI","c":"Paesi","t":"XDAX"},{"y":"XDBC.MI","c":"Materie","t":"XDBC"},{"y":"XDEE.MI","c":"NEW AREA","t":"XDEE"},{"y":"XDER.MI","c":"Tematici","t":"XDER"},{"y":"XDEV.MI","c":"ADVICE","t":"XDEV"},{"y":"XDG3.MI","c":"Tematici","t":"XDG3"},{"y":"XDG6.MI","c":"Tematici","t":"XDG6"},{"y":"XDG7.MI","c":"Tematici","t":"XDG7"},{"y":"XDGI.MI","c":"Tematici","t":"XDGI"},{"y":"XDRE.MI","c":"Settoriali","t":"XDRE"},{"y":"XDW0.MI","c":"Settoriali","t":"XDW0"},{"y":"XDWC.MI","c":"Settoriali","t":"XDWC"},{"y":"XDWF.MI","c":"Settoriali","t":"XDWF"},{"y":"XDWH.MI","c":"Settoriali","t":"XDWH"},{"y":"XDWI.MI","c":"Settoriali","t":"XDWI"},{"y":"XDWM.MI","c":"Settoriali","t":"XDWM"},{"y":"XDWS.MI","c":"Settoriali","t":"XDWS"},{"y":"XDWT.MI","c":"Settoriali","t":"XDWT"},{"y":"XDWU.MI","c":"Settoriali","t":"XDWU"},{"y":"XE01.MI","c":"BOND","t":"XE01"},{"y":"XEON.MI","c":"Liquidita","t":"XEON"},{"y":"XFNT.MI","c":"Tematici","t":"XFNT"},{"y":"XFVT.MI","c":"Paesi","t":"XFVT"},{"y":"XG11.MI","c":"Tematici","t":"XG11"},{"y":"XG12.MI","c":"Tematici","t":"XG12"},{"y":"XGEN.MI","c":"Tematici","t":"XGEN"},{"y":"XGLE.MI","c":"BOND","t":"XGLE"},{"y":"XIFE.MI","c":"Settoriali","t":"XIFE"},{"y":"XLBS.MI","c":"Settoriali","t":"XLBS"},{"y":"XLCS.MI","c":"Settoriali","t":"XLCS"},{"y":"XLES.MI","c":"Settoriali","t":"XLES"},{"y":"XLFS.MI","c":"Settoriali","t":"XLFS"},{"y":"XLIS.MI","c":"Settoriali","t":"XLIS"},{"y":"XLKS.MI","c":"Settoriali","t":"XLKS"},{"y":"XLPE.MI","c":"Tematici","t":"XLPE"},{"y":"XLPS.MI","c":"Settoriali","t":"XLPS"},{"y":"XLUS.MI","c":"Settoriali","t":"XLUS"},{"y":"XLVS.MI","c":"Settoriali","t":"XLVS"},{"y":"XLYS.MI","c":"Settoriali","t":"XLYS"},{"y":"D5BI.DE","c":"Paesi","t":"D5BI"},{"y":"XMME.MI","c":"ADVICE","t":"XMME"},{"y":"XMOV.MI","c":"Tematici","t":"XMOV"},{"y":"XNGI.MI","c":"Tematici","t":"XNGI"},{"y":"XNNV.MI","c":"Tematici","t":"XNNV"},{"y":"XQUI.MI","c":"ATTIVO","t":"XQUI"},{"y":"XRES.MI","c":"Tematici","t":"XRES"},{"y":"XS8R.MI","c":"Tematici","t":"XS8R"},{"y":"XSFR.MI","c":"Paesi","t":"XSFR"},{"y":"XSGI.MI","c":"Tematici","t":"XSGI"},{"y":"XSMI.MI","c":"Paesi","t":"XSMI"},{"y":"XSX6.MI","c":"ADVICE","t":"XSX6"},{"y":"XT01.MI","c":"BOND","t":"XT01"},{"y":"XTC5.MI","c":"BOND","t":"XTC5"},{"y":"XTIP.MI","c":"BOND","t":"XTIP"},{"y":"XUSA.MI","c":"ATTIVO","t":"XUSA"},{"y":"XUTC.MI","c":"Settoriali","t":"XUTC"},{"y":"XWTS.MI","c":"Settoriali","t":"XWTS"},{"y":"XXSC.MI","c":"ATTIVO","t":"XXSC"},{"y":"XYP0.MI","c":"BOND","t":"XYP0"},{"y":"ZINC.MI","c":"Materie","t":"ZINC"},{"y":"EIDO","c":"Paesi","t":"EIDO"},{"y":"EIRL","c":"Paesi","t":"EIRL"},{"y":"IMOM","c":"ATTIVO","t":"IMOM"},{"y":"DBMFE.PA","c":"ATTIVO","t":"DBMFE"},{"y":"MEUD.PA","c":"NEW AREA","t":"MEUD"},{"y":"WRD.PA","c":"Paesi","t":"WRD"},{"y":"IB01.SW","c":"BOND","t":"IB01"},{"y":"SDGPEX.SW","c":"ATTIVO","t":"SDGPEX"},{"y":"X13E.MI","c":"Liquidita","t":"X13E"},{"y":"EM13.MI","c":"Liquidita","t":"EM13"},{"y":"ERNE.MI","c":"Liquidita","t":"ERNE"},{"y":"INFR.MI","c":"Tematici","t":"INFR"},{"y":"swda.MI","c":"benchmark","t":"SWDA_B"},{"y":"xdwd.MI","c":"benchmark","t":"XDWD"},{"y":"cw8.MI","c":"benchmark","t":"CW8"},{"y":"imeu.MI","c":"benchmark","t":"IMEU"},{"y":"inaa.MI","c":"benchmark","t":"INAA"},{"y":"SXLE.MI","c":"SPDR USA","t":"SXLE"},{"y":"MGIN.MI","c":"SPDR USA","t":"MGIN"},{"y":"STWX.MI","c":"SPDR EURO","t":"STWX"},{"y":"STZX.MI","c":"SPDR EURO","t":"STZX"},{"y":"SWRD.MI","c":"benchmark","t":"SWRD"},{"y":"600X.MI","c":"benchmark","t":"600X"},{"y":"EIS","c":"Paesi","t":"EIS"},{"y":"ENZL","c":"Paesi","t":"ENZL"},{"y":"EPHE","c":"Paesi","t":"EPHE"},{"y":"EPI","c":"Paesi","t":"EPI"},{"y":"EPOL","c":"Paesi","t":"EPOL"},{"y":"EPU","c":"Paesi","t":"EPU"},{"y":"EWA","c":"Paesi","t":"EWA"},{"y":"EWC","c":"Paesi","t":"EWC"},{"y":"EWD","c":"Paesi","t":"EWD"},{"y":"EWG","c":"Paesi","t":"EWG"},{"y":"EWH","c":"Paesi","t":"EWH"},{"y":"EWI","c":"Paesi","t":"EWI"},{"y":"EWJ","c":"Paesi","t":"EWJ"},{"y":"EWK","c":"Paesi","t":"EWK"},{"y":"EWL","c":"Paesi","t":"EWL"},{"y":"EWM","c":"Paesi","t":"EWM"},{"y":"EWN","c":"Paesi","t":"EWN"},{"y":"EWO","c":"Paesi","t":"EWO"},{"y":"EWP","c":"Paesi","t":"EWP"},{"y":"EWQ","c":"Paesi","t":"EWQ"},{"y":"EWS","c":"Paesi","t":"EWS"},{"y":"EWT","c":"Paesi","t":"EWT"},{"y":"EWU","c":"Paesi","t":"EWU"},{"y":"EWW","c":"Paesi","t":"EWW"},{"y":"EWY","c":"Paesi","t":"EWY"},{"y":"EWZ","c":"Paesi","t":"EWZ"},{"y":"EZA","c":"Paesi","t":"EZA"},{"y":"FM.TO","c":"Paesi","t":"FM"},{"y":"GREK","c":"Paesi","t":"GREK"},{"y":"GXG","c":"Paesi","t":"GXG"},{"y":"ICLN","c":"Tematici","t":"ICLN"},{"y":"ILF","c":"Paesi","t":"ILF"},{"y":"MES","c":"Paesi","t":"MES"},{"y":"NORW","c":"Paesi","t":"NORW"},{"y":"QQQ","c":"Paesi","t":"QQQ"},{"y":"SPLV","c":"Paesi","t":"SPLV"},{"y":"SPY","c":"Paesi","t":"SPY"},{"y":"THD","c":"Paesi","t":"THD"},{"y":"UAE","c":"Paesi","t":"UAE"},{"y":"VNM","c":"Paesi","t":"VNM"},{"y":"VPL","c":"Paesi","t":"VPL"},{"y":"ADS.DE","c":"EUROGROW","t":"ADS"},{"y":"ADYEN.AS","c":"EUROGROW","t":"ADYEN"},{"y":"AI.PA","c":"EUROGROW","t":"AI"},{"y":"AIR.PA","c":"EUROGROW","t":"AIR"},{"y":"AM.PA","c":"EUROGROW","t":"AM"},{"y":"ARGX","c":"EUROGROW","t":"ARGX"},{"y":"ASM.SW","c":"EUROGROW","t":"ASM"},{"y":"ASML.SW","c":"EUROGROW","t":"ASML"},{"y":"BEI.DE","c":"EUROGROW","t":"BEI"},{"y":"CBK.DE","c":"EUROGROW","t":"CBK"},{"y":"DB1.DE","c":"EUROGROW","t":"DB1"},{"y":"DIM.PA","c":"EUROGROW","t":"DIM"},{"y":"DSY.PA","c":"EUROGROW","t":"DSY"},{"y":"DTE.DE","c":"EUROGROW","t":"DTE"},{"y":"EL.PA","c":"EUROGROW","t":"EL"},{"y":"ELE.MC","c":"EUROGROW","t":"ELE"},{"y":"ENR.DE","c":"EUROGROW","t":"ENR"},{"y":"FER.MC","c":"EUROGROW","t":"FER"},{"y":"HEI.DE","c":"EUROGROW","t":"HEI"},{"y":"HO.PA","c":"EUROGROW","t":"HO"},{"y":"IFX.DE","c":"EUROGROW","t":"IFX"},{"y":"ITX.VI","c":"EUROGROW","t":"ITX"},{"y":"KNEBV.HE","c":"EUROGROW","t":"KNEBV"},{"y":"LDO.MI","c":"EUROGROW","t":"LDO"},{"y":"LR.PA","c":"EUROGROW","t":"LR"},{"y":"MC.PA","c":"EUROGROW","t":"MC"},{"y":"NOKIA.HE","c":"EUROGROW","t":"NOKIA"},{"y":"OR.PA","c":"EUROGROW","t":"OR"},{"y":"PRX.AS","c":"EUROGROW","t":"PRX"},{"y":"PRY.MI","c":"EUROGROW","t":"PRY"},{"y":"RACE.MI","c":"EUROGROW","t":"RACE"},{"y":"RHM.DE","c":"EUROGROW","t":"RHM"},{"y":"RMS.PA","c":"EUROGROW","t":"RMS"},{"y":"RYA.IR","c":"EUROGROW","t":"RYA"},{"y":"SAF.PA","c":"EUROGROW","t":"SAF"},{"y":"SAP.DE","c":"EUROGROW","t":"SAP"},{"y":"SHL.DE","c":"EUROGROW","t":"SHL"},{"y":"SIE.DE","c":"EUROGROW","t":"SIE"},{"y":"SRT.DE","c":"EUROGROW","t":"SRT"},{"y":"STMMI.PA","c":"EUROGROW","t":"STMMI"},{"y":"SU.PA","c":"EUROGROW","t":"SU"},{"y":"UCB","c":"EUROGROW","t":"UCB"},{"y":"UCG.MI","c":"EUROGROW","t":"UCG"},{"y":"UMG.AS","c":"EUROGROW","t":"UMG"},{"y":"WKL.VI","c":"EUROGROW","t":"WKL"}]

# ═══════════════════════════════════════════════════════
#  INDICATORI
# ═══════════════════════════════════════════════════════
def calc_kama(close, n=10, fast=2, slow=30):
    fast_sc = 2/(fast+1)
    slow_sc = 2/(slow+1)
    kama = [None]*len(close)
    if len(close) <= n: return kama
    kama[n] = close[n]
    for i in range(n+1, len(close)):
        direction = abs(close[i] - close[i-n])
        volatility = sum(abs(close[j] - close[j-1]) for j in range(i-n+1, i+1))
        er = direction/volatility if volatility != 0 else 0
        sc = (er*(fast_sc - slow_sc) + slow_sc)**2
        kama[i] = kama[i-1] + sc*(close[i] - kama[i-1])
    return kama

def calc_er(close, n=10):
    if len(close) < n+1: return 0
    direction = abs(close[-1] - close[-n-1])
    volatility = sum(abs(close[-i] - close[-i-1]) for i in range(1, n+1))
    return round(direction/volatility, 4) if volatility != 0 else 0

def calc_rsi(close, n=14):
    if len(close) < n+2: return 50
    gains, losses = [], []
    for i in range(1, len(close)):
        d = close[i] - close[i-1]
        gains.append(max(d,0))
        losses.append(max(-d,0))
    avg_g = sum(gains[-n:])/n
    avg_l = sum(losses[-n:])/n
    if avg_l == 0: return 100
    return round(100 - 100/(1+avg_g/avg_l), 2)

def calc_ao(high, low):
    mid = [(h+l)/2 for h,l in zip(high,low)]
    if len(mid) < 34: return 0
    return round(sum(mid[-5:])/5 - sum(mid[-34:])/34, 4)

def calc_baffetti(high, low):
    if len(high) < 3: return 0
    mid = [(h+l)/2 for h,l in zip(high,low)]
    count = 0
    for i in range(len(mid)-1, 0, -1):
        if mid[i] > mid[i-1]: count += 1
        else: break
    return count

def calc_trendycator(close):
    if len(close) < 55: return 'GRIGIO'
    def ema(arr, p):
        k = 2/(p+1); e = arr[0]
        for x in arr[1:]: e = x*k + e*(1-k)
        return e
    e21 = ema(close, 21)
    e55 = ema(close, 55)
    if e21 > e55: return 'VERDE'
    if e21 < e55: return 'ROSSO'
    return 'GRIGIO'

def calc_vol_ratio(volume):
    if len(volume) < 21: return 1.0
    avg20 = sum(volume[-21:-1])/20
    return round(volume[-1]/avg20, 2) if avg20 > 0 else 1.0

def calc_perf(close, days):
    if len(close) <= days: return 0
    ref = close[-days-1]
    return round((close[-1]/ref - 1)*100, 2) if ref > 0 else 0

def calc_mm_align(close):
    if len(close) < 200: return False
    mm20  = sum(close[-20:])/20
    mm50  = sum(close[-50:])/50
    mm200 = sum(close[-200:])/200
    return close[-1] > mm20 > mm50 > mm200

def calc_cross_days(close, kama):
    valid = [(c,k) for c,k in zip(close,kama) if k is not None]
    if len(valid) < 2: return 999
    above_now = valid[-1][0] > valid[-1][1]
    for i in range(len(valid)-2, -1, -1):
        if (valid[i][0] > valid[i][1]) != above_now:
            return len(valid)-1 - i
    return 999

def calc_entry_date(close, kama, timestamps):
    valid = [(c,k,t) for c,k,t in zip(close,kama,timestamps) if k is not None]
    if len(valid) < 2: return '—'
    above_now = valid[-1][0] > valid[-1][1]
    for i in range(len(valid)-2, -1, -1):
        if (valid[i][0] > valid[i][1]) != above_now:
            dt = datetime.datetime.fromtimestamp(valid[i+1][2])
            return dt.strftime('%d/%m/%Y')
    return '—'

def process_ticker(info):
    symbol = info['y']
    try:
        tk = yf.Ticker(symbol)
        hist = tk.history(period='1y', interval='1d', timeout=15)
        if hist.empty or len(hist) < 60:
            return None

        # Prova a prendere il nome ETF
        nome = info.get('n','')
        if not nome:
            try:
                meta = tk.fast_info
                nome = getattr(meta, 'long_name', '') or getattr(meta, 'short_name', '') or ''
                if not nome:
                    inf = tk.info
                    nome = inf.get('longName','') or inf.get('shortName','') or ''
                nome = nome[:60]  # tronca a 60 chars
            except:
                nome = ''

        close  = [float(x) for x in hist['Close'].values]
        high   = [float(x) for x in hist['High'].values]
        low    = [float(x) for x in hist['Low'].values]
        volume = [float(x) for x in hist['Volume'].values]
        timestamps = [int(t.timestamp()) for t in hist.index]

        kama  = calc_kama(close)
        er    = calc_er(close)
        rsi   = calc_rsi(close)
        ao    = calc_ao(high, low)
        baff  = calc_baffetti(high, low)
        trd   = calc_trendycator(close)
        cross = calc_cross_days(close, kama)
        vr    = calc_vol_ratio(volume)
        ed    = calc_entry_date(close, kama, timestamps)
        mm_align = calc_mm_align(close)

        lk = kama[-1]
        lc = close[-1]
        above_kama = lc > lk if lk else False
        ao_pos = ao > 0
        ao_up = len(high) >= 3 and ((high[-1]+low[-1])/2) > ((high[-2]+low[-2])/2)
        near_kama = abs(lc-lk)/lk < 0.03 if lk and lk > 0 else False

        mr = er < 0.3 and rsi < 30 and ao_up and (near_kama or lc < (lk or lc))

        tipo = ''
        if trd == 'VERDE' and above_kama and er >= 0.50 and baff >= 3 and mm_align:
            tipo = 'LONG'
        elif above_kama and baff >= 3 and trd in ('VERDE','GRIGIO'):
            tipo = 'EARLY'
        elif above_kama and baff >= 1 and trd in ('VERDE','GRIGIO'):
            tipo = 'WATCH'
        elif trd == 'ROSSO' and cross <= 3 and baff >= 3:
            tipo = 'ROSSO+'
        elif mr:
            tipo = 'MR'

        uscita = ''
        if not above_kama and trd == 'ROSSO':
            uscita = 'STOP'
        elif not above_kama:
            uscita = 'USCITA'
        elif above_kama and (not ao_pos or trd == 'GRIGIO'):
            uscita = 'ATTENZIONE'

        pk_pct = round((lc/lk - 1)*100, 2) if lk and lk > 0 else 0
        perf_s = calc_perf(close, 5)
        perf_m = calc_perf(close, 20)

        score = (er*30 + min(baff,10)*5 + min(abs(pk_pct),5)*3
               + max(-10,min(5,perf_s))*4 + max(-20,min(10,perf_m))*2
               + (10 if mm_align else 0) + (5 if ao_pos else 0)
               + (20 if cross<=3 else 12 if cross<=10 else 5 if cross<=20 else 0))
        if trd == 'ROSSO': score *= 0.6

        return {
            'ticker':    info['t'],
            'yahoo':     symbol,
            'categoria': info['c'],
            'nome':      nome,
            'segnale':   tipo,
            'uscita':    uscita,
            'score':     round(score, 1),
            'trendycator': trd,
            'prezzo':    round(lc, 4),
            'kama':      round(lk, 4) if lk else None,
            'er':        er,
            'baff':      baff,
            'kpct':      pk_pct,
            'ao':        round(ao, 4),
            'rsi':       rsi,
            'perfSett':  perf_s,
            'perfMese':  perf_m,
            'volRatio':  vr,
            'crossDays': cross,
            'entryDate': ed,
        }
    except Exception:
        return None

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    print(f"RAPTOR Fetch — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Ticker totali: {len(TICKERS)}")

    results, errors = [], 0

    for i, info in enumerate(TICKERS):
        result = process_ticker(info)
        if result:
            results.append(result)
        else:
            errors += 1
        if (i+1) % 50 == 0:
            print(f"  {i+1}/{len(TICKERS)} — ok:{len(results)} errori:{errors}")
        time.sleep(0.3)  # pausa gentile

    output = {
        'timestamp':    datetime.datetime.now().isoformat(),
        'timestamp_it': datetime.datetime.now().strftime('%d/%m/%Y %H:%M'),
        'total':  len(TICKERS),
        'ok':     len(results),
        'errors': errors,
        'data':   results
    }

    with open('raptor_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, separators=(',',':'))

    print(f"\nSalvato raptor_data.json — {len(results)} OK, {errors} errori")

if __name__ == '__main__':
    main()
