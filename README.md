# qmetry_update_automation
This automation will update QMetry Execution TestCycle using STBT Job runs

# Command to use

  ### Main command will generate pass result from both STBT to QMetry
    python main.py --qmetry_exec_id EXECUTION_ID --stbt_job_category JOB_CATEGORY --compare_file true
 
  ### Main Command to update QMetry from file generated from above command
    python main.py --qmetry_update QMETRY_EXECUTION_ID
  ### The execution ID in QMetry.
    --qmetry_exec_id QMETRY_EXEC_ID
                        
---
  ### The category of the STBT job.
    --stbt_job_category STBT_JOB_CATEGORY
---
  ### The update to be made in QMetry.
    --qmetry_update QMETRY_EXECUTION_ID
---
  ### Will create comparison file with STBT and QMetry
    --compare_file TRUE

