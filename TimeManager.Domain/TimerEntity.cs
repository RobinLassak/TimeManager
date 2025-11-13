using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class TimerEntity : EntityBase
    {
        // Pracovnik
        [Required]
        public EmployeeEntity Employee { get; set; } = null!;


        // Projekt
        [Required]
        public ProjectEntity Project { get; set; } = null!;


        // Datum a cas zacatku
        [Required]
        public DateTime StartTime { get; set; }


        // Datum a cas konce
        public DateTime? EndTime { get; set; }


        // Prestavka zacatek
        public DateTime? BreakStartTime { get; set; }


        // Prestavka konec
        public DateTime? BreakEndTime { get; set; }


        // Popis cinnosti
        [MaxLength(500)]
        public string? Description { get; set; }

    }
}
