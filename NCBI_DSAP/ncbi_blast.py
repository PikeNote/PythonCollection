import requests;
import re;
import time;
import json;

rid_regex = r"^    RID = (.*$)";
rtoe_regex = r"^    RTOE = (.*$)";

waiting_status_regex = r"\s+Status=WAITING";
failed_status_regex = r"\s+Status=FAILED";
unknown_status_regex = r"\s+Status=UNKNOWN";
ready_status_regex = r"\s+Status=READY";

hits_ready_regex = r"\s+ThereAreHits=yes";

def blast(type, database, query):
  url = "https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi";
  payload = {
    "CMD":"Put",
    "PROGRAM": type,
    "DATABASE": database,
    "QUERY":  query
  }
  print("Running a " + type + " for the " + database + "...")

  headers = {'Content-Type': 'application/x-www-form-urlencoded'};
  
  r = requests.post(url, headers=headers, data=payload)
  print("\n")
  print(r.status_code, r.reason)
  print("\n")
  
  rid = re.search(rid_regex, r.text,re.MULTILINE).group(1)
  rtoe = re.search(rtoe_regex, r.text, re.MULTILINE).group(1)
  
  #rid = "6WGW7WXA016";
  #rtoe = "1"

  return getStatus(rid, rtoe);

  #https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?RESULTS_FILE=on&RID=6WGW7WXA016&FORMAT_TYPE=JSON2_S&FORMAT_OBJECT=Alignment&CMD=Get
  
def getResults(rid):
  stat_url = f"https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_TYPE=JSON2_S&RID={rid}";
  r_results = requests.get(stat_url);
  r_json = r_results.json();
  r_json["rid"] = rid;
  return r_json;

  
def getStatus(rid,rtoe):
  status_url = f"https://blast.ncbi.nlm.nih.gov/blast/Blast.cgi?CMD=Get&FORMAT_OBJECT=SearchInfo&RID={rid}"
  print("RID: " + rid)
  print("Estimated time to run: " + rtoe + " seconds");
  print("Waiting for " + rtoe + " seconds before running status check")
  time.sleep(int(rtoe));
  while True:
    time.sleep(10)
    print("Running status check...")
    try:
      r_status = requests.get(status_url);
      if(re.search(waiting_status_regex, r_status.text, re.MULTILINE)):
        pass
        # print("Waiting for results..");
      if(re.search(failed_status_regex, r_status.text, re.MULTILINE)):
        print("Failed running blast. Please try again");
        return {};
        break;
      if(re.search(unknown_status_regex, r_status.text, re.MULTILINE)):
        print("Search has expired. Please try again.");
        return {};
        break;
      if(re.search(ready_status_regex, r_status.text, re.MULTILINE)):
        print("Blast run complete!");
        if(re.search(hits_ready_regex, r_status.text, re.MULTILINE)):
          print("Hits found! Getting results...")
          return getResults(rid);
        else:
          print("No hits found!")
        break;
    except e:
      print("Incomplete read detected.. WiFi is unstable")

