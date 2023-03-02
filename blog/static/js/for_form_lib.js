const educationSelect = document.getElementById('id_education_level');

const supervisorGroup = document.getElementById('supervisor');
const googleScholarGroup = document.getElementById('google_scholar');



educationSelect.addEventListener('change', function() {
  const selectedValue = educationSelect.value;

  if (selectedValue === '3') {
    supervisorGroup.style.display = 'block';
    googleScholarGroup.style.display = 'none';
  } else if (selectedValue === '4'){
    googleScholarGroup.style.display = 'block';
    supervisorGroup.style.display = 'none';
  } else if (selectedValue === '1' || selectedValue === '2'){
    googleScholarGroup.style.display = 'none';
    supervisorGroup.style.display = 'none';
  }
});
