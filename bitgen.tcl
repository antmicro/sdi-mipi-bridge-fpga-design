prj_project open "mipi_tester.ldf"
prj_impl cleanup -impl impl1
prj_run Export -impl impl1 -task Bitgen
prj_project close
