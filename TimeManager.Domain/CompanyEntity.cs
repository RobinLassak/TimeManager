using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    public class CompanyEntity : EntityBase
    {
        // Jmeno firmy
        [Required, MaxLength(100)]
        public string Name { get; set; } = null!;


        // Ico firmy
        [Required, MaxLength(20)]
        public string Ico { get; set; } = null!;


        // Dic firmy
        [MaxLength(20)]
        public string? Dic { get; set; }

    }
}
