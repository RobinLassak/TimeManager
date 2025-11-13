using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class ProjectEntity : EntityBase
    {
        // Nazev projektu
        [Required, MaxLength(100)]
        public string Name { get; set; } = null!;


        // Popis projektu
        [MaxLength(500)]
        public string? Description { get; set; }

        // Zakaznik
        [Required]
        public CustomerEntity Customer { get; set; } = null!;


        // Vedouci projektu
        [Required]
        public EmployeeEntity ProjectManager { get; set; } = null!;


        // Clenove tymu
        public List<EmployeeEntity> TeamMembers { get; set; } = new();


        // Seznam casovych zaznamu
        public List<TimerEntity> Timers { get; set; } = new();


        // Datum zahajeni projektu
        [Required]
        public DateTime StartDate { get; set; }


        // Datum ukonceni projektu
        public DateTime? EndDate { get; set; }


        // Indikator, zda je projekt aktivni
        public bool IsActive => !EndDate.HasValue || EndDate > DateTime.Now;
    }
}
