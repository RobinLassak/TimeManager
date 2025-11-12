using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace TimeManager.Domain
{
    // Bazova entita pro vsechny domenove tridy
    public abstract class EntityBase
    {
        // Unikatni identifikator entity
        [Key]
        public int Id { get; set; }
    }
}
